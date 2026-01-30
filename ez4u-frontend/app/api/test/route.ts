export async function GET(request: Request) {
  try {
    // Proxy request to FastAPI backend
    const response = await fetch('http://localhost:8000/health');

    // Return the FastAPI response
    return new Response(
      JSON.stringify(await response.json()),
      {
        status: response.status,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        error: 'Backend service unavailable',
        details: error instanceof Error ? error.message : 'Unknown error'
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}