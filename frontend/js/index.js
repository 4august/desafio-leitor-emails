import schema from "./schema.js";

class Controller {
  constructor() {
    this.form = document.querySelector("form");
    this.error = document.querySelector("#error");
    this.button = document.querySelector("button[type=submit]");
    this.titleResposta = document.querySelector("h2");
    this.inputFile = document.querySelector("#filePdfTxt");
    this.fileName = document.querySelector("label");

    this.responseContainer = document.querySelector("#response-container");
    this.fileContent = document.querySelector("#file_content");
    this.productivity = document.querySelectorAll("#productivity");
    this.suggestionReply = document.querySelector("#suggestion-reply");
    this.copyReply = document.querySelector("#copy-reply");
    this.anotherSuggestion = document.querySelector("#another-suggestion");

    this.init();

    this.copyReply.addEventListener("click", () => {
      navigator.clipboard.writeText(this.suggestionReply.textContent);

      this.copyReply.textContent = "Copiado";

      setTimeout(() => (this.copyReply.textContent = "Copiar"), 2000);
    });
    this;
  }

  init() {
    this.inputFile.addEventListener("change", () => {
      if (this.inputFile.files.length > 0) {
        this.fileName.innerText = this.inputFile.files[0].name;

        return;
      }
      this.fileName.innerText = "Selecionar Arquivo";
    });

    this.handleSubmitFile();
  }

  handleSubmitFile() {
    this.form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const file = formData.get("filePdfTxt");

      const result = schema.safeParse({
        filePdfTxt: file,
      });

      if (!result.success) {
        this.error.classList.remove("hidden");
        this.error.textContent =
          result.error.flatten().fieldErrors.filePdfTxt[0];
        console.log(result.error.flatten().fieldErrors.filePdfTxt[0]);
        return;
      }

      if (!this.error.className) {
        this.error.classList.add("hidden");
        this.error.textContent = "";
      }

      await this.handleFetchReply(formData);
    });
  }

  async handleFetchReply(formData) {
    try {
      this.titleResposta.innerText = "Gerando Resposta Automática, aguarde...";
      this.titleResposta.classList.remove("hidden");
      this.button.classList.add("hidden");

      const response = await fetch(`http://127.0.0.1:8000/upload-file`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      this.renderAutomaticResponse(result);
    } catch (e) {
      console.error(e);
      this.titleResposta.innerText = "";
      this.titleResposta.classList.add("hidden");
    } finally {
      this.button.classList.remove("hidden");
    }
  }

  renderAutomaticResponse(result) {
    const { file_content, productivity, suggestion_reply } = result;

    this.titleResposta.innerText = "Modelo de Resposta Automática";

    this.responseContainer.innerHTML = `
        <p id="file_content">
            <strong>Conteúdo do Arquivo: </strong>
            ${file_content}
          </p>
        <p id="productivity"><strong>Categoria: </strong>${productivity}</p>
        <div>
            <p id="suggestion-reply">
              <strong>Sugestão de resposta:</strong> 
              ${suggestion_reply}
            </p>
            <button id="copy-reply">Copiar</button>
        </div>
    `;
  }
}

const controller = new Controller();
