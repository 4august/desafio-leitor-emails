import * as z from "https://cdn.jsdelivr.net/npm/zod@4.3.5/+esm";

const TAMANHO_MAX = 1 * 1024 * 1024;
const ARQUIVOS_VALIDOS = ["application/pdf", "text/plain"];
const schema = z.object({
  filePdfTxt: z
    .instanceof(File)
    .refine(
      (file) => file.size <= TAMANHO_MAX,
      "Tamanho máximo de 1MB excedido",
    )
    .refine(
      (file) => ARQUIVOS_VALIDOS.includes(file.type),
      "Somente arquivos .pdf e .txt",
    ),
});

export default schema;
