import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NCAM AgriROS - National Centre for Agricultural Mechanization",
  description: "NCAM Research Intelligence System - Executive & Departmental Portal",
  icons: {
    icon: "/ncam-logo.png",
    shortcut: "/ncam-logo.png",
    apple: "/ncam-logo.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900">{children}</body>
    </html>
  );
}
