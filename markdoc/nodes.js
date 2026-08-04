import { Fence } from '@/components/Fence'
import { nodes as defaultNodes, Tag } from '@markdoc/markdoc'

const nodes = {
  document: {
    render: undefined,
  },
  th: {
    ...defaultNodes.th,
    attributes: {
      ...defaultNodes.th.attributes,
      scope: {
        type: String,
        default: 'col',
      },
    },
  },
  fence: {
    render: Fence,
    attributes: {
      content: { type: String, render: false, required: true },
      language: { type: String },
    },
    // Always render a fence from its raw source, never from transformed children.
    //
    // Markdoc parses `{% … %}` tags *inside* fenced code blocks by default. That makes it
    // impossible to show a Markdoc tag as an example — the tag is interpreted instead of printed,
    // the fence's children become an array of nodes rather than a string, and `Fence` then dies on
    // `children.trimEnd is not a function` during prerender. Docs about this site's own tags are
    // exactly the case that needs to work, so take `content` (the verbatim source) and ignore any
    // children Markdoc produced.
    transform(node, config) {
      const { language } = node.transformAttributes(config)

      return new Tag(Fence, { language }, [node.attributes.content])
    },
  },
}

export default nodes
