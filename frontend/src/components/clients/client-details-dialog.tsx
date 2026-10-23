
"use client";

import { parsePhoneNumberFromString } from "libphonenumber-js";

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

type Client = {
    id: number;
    imie: string;
    nazwisko: string;
    email: string | null;
    telefon: string | null;
};

type ClientDetailsDialogProps = {
    client: Client | null;
    open: boolean;
    onOpenChange: (open: boolean) => void;
};

function formatPhoneNumber(phone: string | null): string {
    if (!phone) return "Brak danych";

    const parsed = parsePhoneNumberFromString(phone, "PL");

    if (!parsed?.isValid()) return phone;

    return parsed.country === "PL"
        ? parsed.formatNational()
        : parsed.formatInternational();
}

export function ClientDetailsDialog({
    client,
    open,
    onOpenChange,
}: ClientDetailsDialogProps) {
    const initials = client
        ? `${client.imie.charAt(0)}${client.nazwisko.charAt(0)}`.toUpperCase()
        : "";

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-h-[85dvh] w-[calc(100%-2rem)] gap-0 overflow-y-auto p-0 sm:max-w-[680px]">

                {/* Nagłówek klienta */}
                <DialogHeader className="flex flex-row items-center gap-4 border-b px-6 py-5 pr-14 text-left">

                    <div
                        aria-hidden="true"
                        className="flex size-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-base font-semibold text-primary"
                    >
                        {initials}
                    </div>

                    <div className="min-w-0 space-y-1">
                        <DialogTitle className="text-lg font-semibold tracking-tight">
                            {client
                                ? `${client.imie} ${client.nazwisko}`
                                : "Kartoteka klienta"}
                        </DialogTitle>

                        <DialogDescription className="text-xs">
                            Kartoteka klienta · ID: {client?.id ?? "—"}
                        </DialogDescription>
                    </div>
                </DialogHeader>

                {client && (
                    <div>

                        {/* Dane osobowe */}
                        <section className="px-6 py-5">
                            <h3 className="mb-5 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                                Dane osobowe
                            </h3>

                            <dl className="grid grid-cols-1 gap-x-8 gap-y-5 sm:grid-cols-2">
                                <div className="space-y-1.5">
                                    <dt className="text-xs text-muted-foreground">
                                        Imię
                                    </dt>
                                    <dd className="text-sm font-medium">
                                        {client.imie}
                                    </dd>
                                </div>

                                <div className="space-y-1.5">
                                    <dt className="text-xs text-muted-foreground">
                                        Nazwisko
                                    </dt>
                                    <dd className="text-sm font-medium">
                                        {client.nazwisko}
                                    </dd>
                                </div>
                            </dl>
                        </section>

                        {/* Dane kontaktowe */}
                        <section className="border-t px-6 py-5">
                            <h3 className="mb-5 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                                Dane kontaktowe
                            </h3>

                            <dl className="grid grid-cols-1 gap-x-8 gap-y-5 sm:grid-cols-2">
                                <div className="min-w-0 space-y-1.5">
                                    <dt className="text-xs text-muted-foreground">
                                        Adres e-mail
                                    </dt>
                                    <dd className="break-all text-sm">
                                        {client.email ? (
                                            <a
                                                href={`mailto:${client.email}`}
                                                className="hover:text-primary hover:underline"
                                            >
                                                {client.email}
                                            </a>
                                        ) : (
                                            <span className="text-muted-foreground">
                                                Brak danych
                                            </span>
                                        )}
                                    </dd>
                                </div>

                                <div className="space-y-1.5">
                                    <dt className="text-xs text-muted-foreground">
                                        Numer telefonu
                                    </dt>
                                    <dd className="text-sm tabular-nums">
                                        {formatPhoneNumber(client.telefon)}
                                    </dd>
                                </div>
                            </dl>
                        </section>

                    </div>
                )}
            </DialogContent>
        </Dialog>
    );
}
