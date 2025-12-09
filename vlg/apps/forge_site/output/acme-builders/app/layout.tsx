import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });
import './globals.css';

export const metadata: Metadata = {
  title: 'Acme Builders',
  description: 'Quality custom home construction and remodels in the Pacific Northwest',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
