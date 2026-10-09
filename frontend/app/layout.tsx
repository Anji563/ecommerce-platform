import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Async E-Commerce Store',
  description: 'E-commerce platform with async processing',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}