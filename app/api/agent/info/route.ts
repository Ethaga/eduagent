import { NextResponse } from "next/server"

export async function GET() {
  return NextResponse.json({
    name: "EduAgent",
    address: "agent1qf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvqxf6ygvq",
    status: "active",
    capabilities: [
      "Mathematical Concept Explanation",
      "Programming Tutorials",
      "Algorithm Analysis",
      "Data Structure Guidance",
      "Practice Problem Generation",
    ],
  })
}
