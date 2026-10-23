"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
} from "@/components/ui/card";

type TestMessage = {
    id: number;
    message: string;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function ConnectionTestPage() {
    const [status, setStatus] = useState("Nie sprawdzono");
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState<TestMessage[]>([]);

    // 1. Sprawdzenie połączenia FastAPI z Supabase
    async function checkConnection() {
        try {
            const response = await fetch(`${API_URL}/api/db-check`);

            if (!response.ok) {
                throw new Error("Błąd połączenia");
            }

            const data = await response.json();
            setStatus(data.database);
        } catch {
            setStatus("Nie udało się połączyć z bazą");
        }
    }

    // 2. Zapis wiadomości do Supabase przez FastAPI
    async function saveMessage() {
        try {
            const response = await fetch(`${API_URL}/api/test-messages`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    message: message.trim(),
                }),
            });

            if (!response.ok) {
                throw new Error("Błąd zapisu");
            }

            setMessage("");
            setStatus("Wiadomość została zapisana");
        } catch {
            setStatus("Nie udało się zapisać wiadomości");
        }
    }

    // 3. Odczyt wiadomości z Supabase przez FastAPI
    async function loadMessages() {
        try {
            const response = await fetch(`${API_URL}/api/test-messages`);

            if (!response.ok) {
                throw new Error("Błąd odczytu");
            }

            const data: TestMessage[] = await response.json();

            setMessages(data);
            setStatus("Wiadomości zostały pobrane");
        } catch {
            setStatus("Nie udało się pobrać wiadomości");
        }
    }

    return (
        <main className="flex min-h-screen items-center justify-center bg-background p-6">
            <Card className="w-full max-w-lg">
                <CardHeader>
                    <CardTitle>Studio Fitness B — Test połączenia</CardTitle>
                </CardHeader>

                <CardContent className="space-y-6">
                    {/* Sprawdzenie połączenia */}
                    <section className="space-y-3">
                        <h2 className="text-lg font-semibold">
                            1. Sprawdzenie połączenia
                        </h2>

                        <Button onClick={checkConnection}>
                            Sprawdź połączenie
                        </Button>

                        <p className="text-sm text-muted-foreground" aria-live="polite">
                            Status: {status}
                        </p>
                    </section>

                    {/* Zapis danych */}
                    <section className="space-y-3">
                        <h2 className="text-lg font-semibold">
                            2. Zapis danych
                        </h2>

                        <Input
                            placeholder="Wpisz wiadomość testową"
                            value={message}
                            onChange={(e) => setMessage(e.target.value)}
                        />

                        <Button
                            onClick={saveMessage}
                            disabled={!message.trim()}
                        >
                            Zapisz w Supabase
                        </Button>
                    </section>

                    {/* Odczyt danych */}
                    <section className="space-y-3">
                        <h2 className="text-lg font-semibold">
                            3. Odczyt danych
                        </h2>

                        <Button variant="outline" onClick={loadMessages}>
                            Pobierz wiadomości
                        </Button>

                        <ul className="space-y-2">
                            {messages.map((item) => (
                                <li
                                    key={item.id}
                                    className="rounded-md border p-3 text-sm"
                                >
                                    {item.id}: {item.message}
                                </li>
                            ))}
                        </ul>
                    </section>
                </CardContent>
            </Card>
        </main>
    );
}