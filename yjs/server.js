import { Server } from "@hocuspocus/server";
import { Database } from "@hocuspocus/extension-database";
import pg from "pg";
import dotenv from "dotenv";
import * as Y from "yjs";

dotenv.config();
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

const SAVE_INTERVAL = Number(process.env.SAVE_INTERVAL) || 30000;

const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
});

const activeDocuments = new Map();

const server = new Server({
  port: process.env.PORT || 1234,
  address: process.env.SERVER_IP,

  async onAuthenticate({ token }) {
    if (!token) return false;

    try {
      const response = await fetch(`${process.env.FASTAPI_URL}/user/profile`, {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) return false;

      const user = await response.json();
      return { userId: user.id };
    } catch (err) {
      console.log("[Auth] Ошибка при проверке токена", err.message);
      return false;
    }
  },

  async onLoadDocument({ documentName, document }) {
    activeDocuments.set(documentName, document);
    console.log(
      `[onLoadDocument] Документ ${documentName} загружен и добавлен в активные`,
    );
  },
  async onDisconnect({ documentName, userId }) {
    console.log(
      `[onDisconnect] Пользователь ${userId} отключился из документа ${documentName}`,
    );

    const doc = activeDocuments.get(documentName);
    if (!doc) return;

    const remainingClients = doc.getClients().size;
    if (remainingClients === 0) {
      try {
        const state = Y.encodeStateAsUpdate(doc);
        await pool.query("UPDATE document SET yjs_updates = $1 WHERE id = $2", [
          state,
          documentName,
        ]);
        console.log(
          `[onDisconnect] Документ ${documentName} сохранён (последний пользователь вышел)`,
        );
        activeDocuments.delete(documentName);
      } catch (err) {
        console.error("[onDisconnect] Ошибка сохранения документа:", err);
      }
    }
  },

  extensions: [
    new Database({
      async fetch({ documentName }) {
        const { rows } = await pool.query(
          "SELECT yjs_updates FROM document WHERE id = $1",
          [documentName],
        );
        const data = rows[0]?.yjs_updates;
        if (!data) return null;

        return new Uint8Array(data);
      },

      async store({ documentName, state }) {
        await pool.query("UPDATE document SET yjs_updates = $1 WHERE id = $2", [
          state,
          documentName,
        ]);
      },
    }),
  ],
});

setInterval(async () => {
  try {
    for (const [documentName, doc] of activeDocuments.entries()) {
      const state = Y.encodeStateAsUpdate(doc);
      await pool.query("UPDATE document SET yjs_updates = $1 WHERE id = $2", [
        state,
        documentName,
      ]);
      console.log(`[autosave] Документ ${documentName} сохранён`);
    }
  } catch (err) {
    console.error("[autosave] Ошибка автосохранения документов:", err);
  }
}, SAVE_INTERVAL);

server.listen();
console.log(`Hocuspocus running on port ${process.env.PORT || 1234}`);
