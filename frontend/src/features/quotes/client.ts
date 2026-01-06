export async function fetchQuotes() {
  const res = await fetch('/api/quotes')

  if (!res.ok) {
    throw new Error('Failed to fetch quotes')
  }

  const data = await res.json()
  return Array.isArray(data?.quotes) ? data.quotes : []
}
