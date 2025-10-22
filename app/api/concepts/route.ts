import { NextResponse } from "next/server"

export async function GET() {
  return NextResponse.json({
    concepts: [
      "algebra",
      "calculus",
      "geometry",
      "statistics",
      "python",
      "javascript",
      "data-structures",
      "algorithms",
    ],
  })
}
