export async function GET() {
  const res = await fetch(
    `${process.env.FASTAPI_URL}/api/quotes`,
    { cache: 'no-store' }
  )

  if (!res.ok) {
    return Response.json(
      { message: 'Failed to fetch quotes' },
      { status: 500 }
    )
  }

  const data = await res.json()
  return Response.json(data)
}
