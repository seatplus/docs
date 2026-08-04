#!/usr/bin/env python3
"""Import browser-test screenshots from the seatplus/core package into this docs site.

The core package's browser suite (`composer run browser` in the core checkout) captures a
full-page PNG per view per viewport via the `snap()` helper, writing them to
`tests/Browser/Screenshots/<name>-<desktop|iphone>.png`.

Those captures are 1728x1117 regardless of how tall the page content actually is, so most of
them are 30-70% empty canvas. This script crops each one to its content and copies it here
under a documentation-friendly name.

Cropping is content-aware rather than a plain bounding-box trim: the app's dark sidebar runs
the full height of every capture, so a naive trim never removes anything vertically, while
measuring only the main content column cuts the sidebar navigation off mid-list (and that
navigation is exactly what tells a reader where a feature lives). So we measure both columns
against their own background colour, and ignore the fixed user-card band at the very bottom
of the sidebar.

Usage:
    python scripts/import_screenshots.py [--source DIR] [--dry-run]

Only the screenshots listed in MANIFEST are imported; anything else in the source directory is
ignored, and a missing entry is a hard error rather than a silent skip.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow is required: pip install Pillow")

DEFAULT_SOURCE = Path(
    "/Users/hufe/PhpstormProjects/seatplus/core/tests/Browser/Screenshots"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEST_ROOT = REPO_ROOT / "public" / "images"

# Width of the app's dark sidebar in the desktop captures.
SIDEBAR_WIDTH = 256
# The sidebar's bottom user card is pinned to the viewport bottom, so it would defeat any
# vertical crop. Ignore that band when looking for the last row of real content.
FOOTER_BAND = 110
# Breathing room kept below the last content row.
PADDING = 36
# Per-channel tolerance when deciding whether a pixel differs from its region's background.
TOLERANCE = 8
# Horizontal sampling stride. The captures are 1728px wide; every 7th pixel is plenty to
# notice a text row while keeping the scan fast.
STRIDE = 7

# stem in the core Screenshots dir (without the "-desktop" suffix)  ->  path under public/images
MANIFEST: dict[str, str] = {
    # ---------------------------------------------------------------- getting started
    "login": "first-run/login.png",
    "dashboard": "first-run/dashboard.png",
    # ---------------------------------------------------------------- concepts
    "dashboard-multiple-characters": "concepts/dashboard-multiple-characters.png",
    "entity-picker-open": "concepts/entity-picker.png",
    "entity-picker-selection-applied": "concepts/entity-picker-applied.png",
    # ---------------------------------------------------------------- control groups
    "hub-index-admin": "control-groups/hub-admin.png",
    "hub-index-moderator": "control-groups/hub-moderator.png",
    "hub-index-member": "control-groups/hub-member.png",
    "hub-index-eligible": "control-groups/hub-eligible.png",
    "hub-index-nonmember": "control-groups/hub-nonmember.png",
    "hub-overview-admin": "control-groups/overview-admin.png",
    "hub-overview-member": "control-groups/overview-member.png",
    "hub-members-admin": "control-groups/members-admin.png",
    "hub-members-moderator": "control-groups/members-moderator.png",
    "hub-configure-admin": "control-groups/configure-admin.png",
    "acl-create-wizard": "control-groups/create-wizard.png",
    "acl-create-wizard-everyone": "control-groups/create-wizard-everyone.png",
    # ---------------------------------------------------------------- recruitment
    "recruitment-manage": "recruitment/manage-posting.png",
    "recruitment-portal": "recruitment/job-portal.png",
    "recruitment-my-application": "recruitment/my-application.png",
    "recruitment-reviews-junior": "recruitment/reviews-junior.png",
    "recruitment-reviews-junior-empty": "recruitment/reviews-junior-empty.png",
    "recruitment-reviews-senior": "recruitment/reviews-senior.png",
    "recruitment-review-detail": "recruitment/review-detail.png",
    "recruitment-review-tab-skills": "recruitment/review-tab-skills.png",
    "recruitment-review-tab-wallets": "recruitment/review-tab-wallets.png",
    "recruitment-review-tab-assets": "recruitment/review-tab-assets.png",
    "recruitment-review-tab-corporation-history": "recruitment/review-tab-corporation-history.png",
    "recruitment-review-tab-contracts": "recruitment/review-tab-contracts.png",
    "recruitment-review-update-character": "recruitment/review-update-character.png",
    # ---------------------------------------------------------------- personnel
    "corporation-member-tracking-infinite-scroll": "personnel/member-tracking.png",
    "observation": "personnel/observation.png",
    "observation-inspect": "personnel/observation-inspect.png",
    # ---------------------------------------------------------------- character data
    "character-assets-infinite-scroll": "character/assets.png",
    "character-assets-search": "character/assets-search.png",
    "character-assets-region-filter": "character/assets-region-filter.png",
    "character-assets-contents-modal": "character/assets-contents-modal.png",
    "character-assets-asset-safety": "character/assets-asset-safety.png",
    "character-assets-deeplink-depth-three": "character/assets-deeplink.png",
    "character-contacts": "character/contacts.png",
    "character-contracts-infinite-scroll": "character/contracts.png",
    "character-contracts-assignee-acceptor": "character/contracts-assignee-acceptor.png",
    "character-mails-infinite-scroll": "character/mails.png",
    "character-skills": "character/skills.png",
    "character-skills-empty-queue": "character/skills-empty-queue.png",
    "character-wallet-infinite-scroll": "character/wallet.png",
    "character-wallet-filter": "character/wallet-filter.png",
    # ---------------------------------------------------------------- corporation data
    "corporation-wallet-infinite-scroll": "corporation/wallet.png",
    "manual-locations-lifecycle-1-unknown": "corporation/manual-locations-1-unknown.png",
    "manual-locations-lifecycle-2-add": "corporation/manual-locations-2-suggest.png",
    "manual-locations-lifecycle-3-review": "corporation/manual-locations-3-review.png",
    "manual-locations-lifecycle-4-resolved": "corporation/manual-locations-4-resolved.png",
    # ---------------------------------------------------------------- administration
    "settings-navigation": "administration/server-settings.png",
    "dispatch-owned-character": "administration/dispatch-owned-character.png",
    "dispatch-affiliated-character": "administration/dispatch-affiliated-character.png",
    "dispatch-owned-corporation": "administration/dispatch-owned-corporation.png",
}


def last_content_row(image: Image.Image) -> int:
    """Return the y of the lowest row holding content, ignoring the sidebar's footer band."""
    width, height = image.size
    pixels = image.load()

    main_bg = pixels[width - 5, height - 5]
    sidebar_bg = pixels[SIDEBAR_WIDTH // 2, height // 2]

    last = 0
    for y in range(max(0, height - FOOTER_BAND)):
        for x in range(4, width, STRIDE):
            background = sidebar_bg if x < SIDEBAR_WIDTH else main_bg
            pixel = pixels[x, y]
            if any(abs(pixel[c] - background[c]) > TOLERANCE for c in range(3)):
                last = y
                break

    return last


def crop_to_content(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    width, height = image.size
    bottom = min(height, last_content_row(image) + PADDING)

    return image.crop((0, 0, width, bottom))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="core package's tests/Browser/Screenshots directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would be written without touching any file",
    )
    args = parser.parse_args()

    if not args.source.is_dir():
        print(f"error: source directory not found: {args.source}", file=sys.stderr)
        print(
            "hint: run `composer run browser` in the core checkout to produce the captures.",
            file=sys.stderr,
        )
        return 1

    missing = [
        stem
        for stem in MANIFEST
        if not (args.source / f"{stem}-desktop.png").is_file()
    ]
    if missing:
        print(
            f"error: {len(missing)} capture(s) missing from {args.source}:", file=sys.stderr
        )
        for stem in missing:
            print(f"  {stem}-desktop.png", file=sys.stderr)
        print(
            "hint: re-run `composer run browser` in the core checkout — the browser suite "
            "must pass for every view listed in the manifest.",
            file=sys.stderr,
        )
        return 1

    total_bytes = 0
    print(f"{'source':<50} {'destination':<52} {'size':>12}")
    print("-" * 116)

    for stem, relative in sorted(MANIFEST.items(), key=lambda item: item[1]):
        source = args.source / f"{stem}-desktop.png"
        destination = DEST_ROOT / relative
        cropped = crop_to_content(source)

        if not args.dry_run:
            destination.parent.mkdir(parents=True, exist_ok=True)
            cropped.save(destination, "PNG", optimize=True)
            total_bytes += destination.stat().st_size

        original = Image.open(source).size
        print(
            f"{stem:<50} {relative:<52} "
            f"{original[0]}x{original[1]} -> {cropped.size[0]}x{cropped.size[1]}"
        )

    print("-" * 116)
    verb = "would import" if args.dry_run else "imported"
    footprint = "" if args.dry_run else f", {total_bytes / 1024 / 1024:.1f} MB on disk"
    print(f"{verb} {len(MANIFEST)} screenshot(s){footprint}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
