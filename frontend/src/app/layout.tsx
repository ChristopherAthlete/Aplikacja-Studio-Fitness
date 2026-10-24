import type { Metadata } from "next";
import { Geist, Geist_Mono, Inter } from "next/font/google";
import "./globals.css";
import { cn } from "@/lib/utils";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AppSidebar } from "@/components/app-sidebar";
import {
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
} from "@/components/ui/sidebar";

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

const interHeading = Inter({ subsets: ['latin'], variable: '--font-heading' });

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Studio Fitness",
  description: "System zarządzania studiem fitness",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="pl"
      className={cn("h-full", "antialiased", geistSans.variable, geistMono.variable, interHeading.variable, "font - sans", inter.variable)}
    >
      <body className="min-h-full flex flex-col">
        <TooltipProvider>
          <SidebarProvider>
            <AppSidebar />

            <SidebarInset>
              <header className="flex h-16 shrink-0 items-center gap-4 border-b px-6">
                <SidebarTrigger />

                <span className="text-sm font-medium">
                  Studio Fitness
                </span>
              </header>

              <div className="flex flex-1 flex-col p-6">
                {children}
              </div>
            </SidebarInset>
          </SidebarProvider>
        </TooltipProvider>
      </body>
    </html >
  );
}
