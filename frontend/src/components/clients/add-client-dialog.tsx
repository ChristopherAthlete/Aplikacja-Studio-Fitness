
"use client";

import { useState, type FormEvent } from "react";
import {
    AsYouType,
    parsePhoneNumberFromString,
} from "libphonenumber-js";

import { PlusIcon } from "@phosphor-icons/react";

import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
    DialogClose,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type AddClientDialogProps = {
    onClientAdded: () => void;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export function AddClientDialog({
    onClientAdded,
}: AddClientDialogProps) {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [phone, setPhone] = useState("");

    // Formatowanie telefonu w trakcie wpisywania
    function handlePhoneChange(value: string) {
        setPhone(new AsYouType("PL").input(value));
    }

    function handleOpenChange(nextOpen: boolean) {
        setOpen(nextOpen);

        if (!nextOpen) {
            setError("");
            setPhone("");
        }
    }

    // Zapis klienta przez FastAPI
    async function handleSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();

        const form = event.currentTarget;
        const formData = new FormData(form);

        const imie = String(formData.get("imie") ?? "").trim();
        const nazwisko = String(formData.get("nazwisko") ?? "").trim();
        const email = String(formData.get("email") ?? "").trim();

        if (!imie || !nazwisko) {
            setError("Imię i nazwisko są wymagane.");
            return;
        }

        const parsedPhone = phone
            ? parsePhoneNumberFromString(phone, "PL")
            : undefined;

        if (phone && !parsedPhone?.isValid()) {
            setError("Podaj poprawny numer telefonu.");
            return;
        }

        const client = {
            imie,
            nazwisko,
            email: email || null,
            telefon: parsedPhone?.number ?? null,
        };

        setLoading(true);
        setError("");

        try {
            const response = await fetch(`${API_URL}/api/clients`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(client),
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            // Czyszczenie formularza
            form.reset();
            setPhone("");

            // Zamknięcie okna
            setOpen(false);

            // Aktualizacja tabeli
            onClientAdded();
        } catch (err) {
            console.error("Błąd dodawania klienta:", err);
            setError("Nie udało się zapisać klienta.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <Dialog open={open} onOpenChange={handleOpenChange}>
            {/* Przycisk na pasku narzędzi */}
            <DialogTrigger
                render={<Button size="sm" type="button" />}
            >
                <PlusIcon className="size-4" />
                Dodaj klienta
            </DialogTrigger>

            <DialogContent className="sm:max-w-lg">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <DialogHeader>
                        <DialogTitle>Dodaj klienta</DialogTitle>
                        <DialogDescription>
                            Wprowadź podstawowe dane nowego klienta.
                        </DialogDescription>
                    </DialogHeader>

                    <div className="space-y-4">
                        {/* Imię i nazwisko */}
                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                            <div className="space-y-2">
                                <Label htmlFor="client-imie">Imię *</Label>
                                <Input
                                    id="client-imie"
                                    name="imie"
                                    placeholder="Jan"
                                    maxLength={60}
                                    required
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="client-nazwisko">
                                    Nazwisko *
                                </Label>
                                <Input
                                    id="client-nazwisko"
                                    name="nazwisko"
                                    placeholder="Kowalski"
                                    maxLength={80}
                                    required
                                />
                            </div>
                        </div>

                        {/* E-mail */}
                        <div className="space-y-2">
                            <Label htmlFor="client-email">
                                Adres e-mail
                            </Label>
                            <Input
                                id="client-email"
                                name="email"
                                type="email"
                                placeholder="jan@example.com"
                                maxLength={254}
                            />
                        </div>

                        {/* Telefon */}
                        <div className="space-y-2">
                            <Label htmlFor="client-telefon">
                                Telefon
                            </Label>
                            <Input
                                id="client-telefon"
                                name="telefon"
                                type="tel"
                                autoComplete="tel"
                                placeholder="512 000 000"
                                value={phone}
                                onChange={(e) =>
                                    handlePhoneChange(e.target.value)
                                }
                                maxLength={30}
                            />
                            <p className="text-xs text-muted-foreground">
                                Dla numerów zagranicznych podaj prefiks,
                                np. +1 lub +44.
                            </p>
                        </div>
                    </div>

                    {/* Komunikat błędu */}
                    {error && (
                        <p
                            className="text-sm text-destructive"
                            role="alert"
                        >
                            {error}
                        </p>
                    )}

                    {/* Przyciski */}
                    <DialogFooter>
                        <DialogClose
                            render={
                                <Button
                                    variant="outline"
                                    type="button"
                                    disabled={loading}
                                />
                            }
                        >
                            Anuluj
                        </DialogClose>

                        <Button type="submit" disabled={loading}>
                            {loading ? "Zapisywanie..." : "Zapisz klienta"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
