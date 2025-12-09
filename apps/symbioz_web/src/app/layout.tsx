import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Mellivox - Honeyvoice of the Pact',
  description: 'Symbiosis produces consequence. Every connection changes reality.',
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

