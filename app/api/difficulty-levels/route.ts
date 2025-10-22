import { NextResponse } from "next/server"

export async function GET() {
  return NextResponse.json({
    levels: ["beginner", "intermediate", "advanced"],
  })
}
