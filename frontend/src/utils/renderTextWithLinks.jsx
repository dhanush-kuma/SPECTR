const URL_SPLIT_PATTERN = /(https?:\/\/[^\s<>"']+)/g
const URL_TEST_PATTERN = /^https?:\/\/[^\s<>"']+$/

export function renderTextWithLinks(text) {
  if (!text) return null

  const parts = text.split(URL_SPLIT_PATTERN)

  return parts.map((part, index) => {
    if (URL_TEST_PATTERN.test(part)) {
      return (
        <a
          key={`link-${index}`}
          href={part}
          target="_blank"
          rel="noopener noreferrer"
        >
          {part}
        </a>
      )
    }

    return part
  })
}
