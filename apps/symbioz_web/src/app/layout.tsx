import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Symbioz - Sci-Fi RPG',
  description: 'A KOTOR-inspired text-based RPG',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

