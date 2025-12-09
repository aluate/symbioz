import type { Metadata } from 'next'
import { Playfair_Display, Inter } from 'next/font/google'
import './styles/globals.css'
import Header from './components/Header'
import Footer from './components/Footer'

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
})

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Sugar Mountain Builders – Mountain-Modern Homes in the Inland Northwest',
  description: 'Mountain-modern homes, modular installs, and reliable construction services across the Inland Northwest. Sugar Mountain Builders delivers precision-crafted homes built for mountain living.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${playfair.variable} ${inter.variable}`}>
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  )
}
