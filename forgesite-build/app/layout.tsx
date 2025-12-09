import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Forge Site - Clean Websites for Builders & Trades',
  description: 'Get seen. Stay simple. Clean websites built fast for builders, trades, and shops.',
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
