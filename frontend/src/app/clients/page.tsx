
"use client";

import { useEffect, useState } from "react";
import { parsePhoneNumberFromString } from "libphonenumber-js";

import {
    ListBulletsIcon,
    MagnifyingGlassIcon,
    XIcon,
} from "@phosphor-icons/react";

import { AddClientDialog } from "@/components/clients/add-client-dialog";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import { ClientDetailsDialog } from "@/components/clients/client-details-dialog";

// Typ danych klienta pobieranego z FastAPI
type Client = {
    id: number;
    imie: string;
    nazwisko: string;
    email: string | null;
    telefon: string | null;
};

const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Formatowanie numeru telefonu
function formatPhoneNumber(phone: string | null): string {
    if (!phone) return "—";

    const parsed = parsePhoneNumberFromString(phone, "PL");

    if (!parsed?.isValid()) return phone;

    return parsed.country === "PL"
        ? parsed.formatNational()
        : parsed.formatInternational();
}

export default function ClientsPage() {
    // Dane klientów
    const [clients, setClients] = useState<Client[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Wyszukiwanie
    const [search, setSearch] = useState("");
    const [searchOpen, setSearchOpen] = useState(false);

    // Odświeżanie listy po dodaniu klienta
    const [refreshKey, setRefreshKey] = useState(0);

    // Aktualnie wybrany klient
    const [selectedClient, setSelectedClient] =
        useState<Client | null>(null);

    // Pobieranie klientów z FastAPI
    useEffect(() => {
        const controller = new AbortController();

        fetch(`${API_URL}/api/clients`, {
            cache: "no-store",
            signal: controller.signal,
        })
            .then(async (response) => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                return (await response.json()) as Client[];
            })
            .then((data) => {
                if (controller.signal.aborted) return;

                setClients(data);
                setError("");
            })
            .catch((err) => {
                if (controller.signal.aborted) return;

                console.error("Błąd pobierania klientów:", err);
                setError("Nie udało się pobrać klientów.");
            })
            .finally(() => {
                if (!controller.signal.aborted) {
                    setLoading(false);
                }
            });

        return () => controller.abort();
    }, [refreshKey]);

    // Ponowne pobranie danych po dodaniu klienta
    function handleClientAdded() {
        setLoading(true);
        setRefreshKey((previous) => previous + 1);
    }

    // Filtrowanie klientów
    const filteredClients = clients.filter((client) => {
        const query = search.trim().toLowerCase();

        const searchableText = [
            client.id,
            client.imie,
            client.nazwisko,
            client.email,
            client.telefon,
        ]
            .filter((value) => value != null)
            .join(" ")
            .toLowerCase();

        const phoneQuery = query.replace(/\D/g, "");
        const phoneDigits =
            client.telefon?.replace(/\D/g, "") ?? "";

        return (
            searchableText.includes(query) ||
            (phoneQuery.length > 0 &&
                /^[+\d\s()-]+$/.test(query) &&
                phoneDigits.includes(phoneQuery))
        );
    });

    // Zamykanie wyszukiwarki
    function closeSearch() {
        setSearch("");
        setSearchOpen(false);
    }

    // Otwieranie kartoteki klienta
    function openClientDetails(client: Client) {
        setSelectedClient(client);
    }

    // Zamykanie kartoteki klienta
    function handleSheetOpenChange(open: boolean) {
        if (!open) {
            setSelectedClient(null);
        }
    }

    return (
        <main className="flex w-full flex-col gap-4">
            {/* Nagłówek strony */}
            <div>
                <h1 className="text-xl font-semibold tracking-tight">
                    Klienci
                </h1>

                <p className="text-sm text-muted-foreground">
                    Zarządzanie klientami studia fitness
                </p>
            </div>

            {/* Pasek widoku i akcji */}
            <div className="flex min-h-11 flex-wrap items-center justify-between gap-3 border-b">
                {/* Aktywny widok */}
                <div className="flex h-11 items-center border-b-2 border-primary px-2">
                    <ListBulletsIcon className="mr-2 size-4" />
                    <span className="text-sm font-medium">
                        Lista
                    </span>
                </div>

                {/* Akcje */}
                <div className="flex items-center gap-2 pb-1">
                    {/* Wyszukiwanie */}
                    {searchOpen ? (
                        <div className="flex items-center gap-1">
                            <Input
                                autoFocus
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                placeholder="Szukaj klientów..."
                                aria-label="Szukaj klientów"
                                className="h-8 w-44 sm:w-60"
                                onKeyDown={(e) => {
                                    if (e.key === "Escape") {
                                        closeSearch();
                                    }
                                }}
                            />

                            <Button
                                type="button"
                                variant="ghost"
                                size="icon-sm"
                                aria-label="Zamknij wyszukiwanie"
                                onClick={closeSearch}
                            >
                                <XIcon className="size-4" />
                            </Button>
                        </div>
                    ) : (
                        <Button
                            type="button"
                            variant="ghost"
                            size="icon-sm"
                            aria-label="Szukaj klientów"
                            title="Szukaj klientów"
                            onClick={() => setSearchOpen(true)}
                        >
                            <MagnifyingGlassIcon className="size-4" />
                        </Button>
                    )}

                    {/* Dodawanie klienta */}
                    <AddClientDialog
                        onClientAdded={handleClientAdded}
                    />
                </div>
            </div>

            {/* Tabela klientów */}
            <div className="overflow-hidden rounded-lg border">
                <Table className="w-full min-w-180 table-fixed">
                    <TableHeader className="bg-muted/20">
                        <TableRow className="hover:bg-transparent">
                            <TableHead className="w-[8%] pl-4">
                                ID
                            </TableHead>

                            <TableHead className="w-[32%]">
                                Imię i nazwisko
                            </TableHead>

                            <TableHead className="w-[38%]">
                                E-mail
                            </TableHead>

                            <TableHead className="w-[22%]">
                                Telefon
                            </TableHead>
                        </TableRow>
                    </TableHeader>

                    <TableBody>
                        {loading ? (
                            <TableRow>
                                <TableCell
                                    colSpan={4}
                                    className="py-8 text-center text-muted-foreground"
                                >
                                    Ładowanie klientów...
                                </TableCell>
                            </TableRow>
                        ) : error ? (
                            <TableRow>
                                <TableCell
                                    colSpan={4}
                                    className="py-8 text-center text-destructive"
                                >
                                    {error}
                                </TableCell>
                            </TableRow>
                        ) : filteredClients.length === 0 ? (
                            <TableRow>
                                <TableCell
                                    colSpan={4}
                                    className="py-8 text-center text-muted-foreground"
                                >
                                    {search.trim()
                                        ? "Nie znaleziono klientów."
                                        : "Brak klientów w bazie."}
                                </TableCell>
                            </TableRow>
                        ) : (
                            filteredClients.map((client) => (
                                <TableRow
                                    key={client.id}
                                    className="h-11 cursor-pointer hover:bg-muted/40"
                                    onClick={() => openClientDetails(client)}
                                >
                                    {/* ID */}
                                    <TableCell className="pl-4 text-muted-foreground">
                                        {client.id}
                                    </TableCell>

                                    {/* Imię i nazwisko */}
                                    <TableCell>
                                        <button
                                            type="button"
                                            className="block w-full truncate text-left font-medium hover:underline focus-visible:rounded-sm focus-visible:outline-2 focus-visible:outline-ring"
                                            aria-label={`Otwórz kartotekę: ${client.imie} ${client.nazwisko}`}
                                            onClick={(event) => {
                                                event.stopPropagation();
                                                openClientDetails(client);
                                            }}
                                        >
                                            {client.imie} {client.nazwisko}
                                        </button>
                                    </TableCell>

                                    {/* E-mail */}
                                    <TableCell className="text-muted-foreground">
                                        <span className="block truncate">
                                            {client.email ?? "—"}
                                        </span>
                                    </TableCell>

                                    {/* Telefon */}
                                    <TableCell className="text-muted-foreground">
                                        {formatPhoneNumber(client.telefon)}
                                    </TableCell>
                                </TableRow>
                            ))
                        )}
                    </TableBody>
                </Table>
            </div>

            {/* Licznik klientów */}
            <div className="text-xs text-muted-foreground">
                {loading || error
                    ? "—"
                    : search.trim()
                        ? `Znaleziono: ${filteredClients.length} z ${clients.length}`
                        : `Liczba klientów: ${clients.length}`}
            </div>

            {/* Panel szczegółów klienta */}
            <ClientDetailsDialog
                client={selectedClient}
                open={selectedClient !== null}
                onOpenChange={handleSheetOpenChange}
            />
        </main>
    );
}
