const fileInput = document.querySelector("#fileInput");
const dropZone = document.querySelector("#dropZone");
const dropTitle = document.querySelector("#dropTitle");
const dropHint = document.querySelector("#dropHint");
const widthInput = document.querySelector("#widthInput");
const widthOutput = document.querySelector("#widthOutput");
const charSet = document.querySelector("#charSet");
const invertInput = document.querySelector("#invertInput");
const copyButton = document.querySelector("#copyButton");
const downloadButton = document.querySelector("#downloadButton");
const asciiOutput = document.querySelector("#asciiOutput");
const emptyState = document.querySelector("#emptyState");
const sizeLabel = document.querySelector("#sizeLabel");
const canvas = document.querySelector("#imageCanvas");
const toast = document.querySelector("#toast");
const replaceButton = document.querySelector("#replaceButton");

let currentFile = null;
let currentAscii = "";
let toastTimer = null;

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 1800);
}

function loadImage(file) {
  return new Promise((resolve, reject) => {
    if (!file.type.startsWith("image/")) {
      reject(new Error("请选择图片文件"));
      return;
    }

    const url = URL.createObjectURL(file);
    const image = new Image();

    image.onload = () => {
      URL.revokeObjectURL(url);
      resolve(image);
    };

    image.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("无法读取这张图片"));
    };

    image.src = url;
  });
}

async function processFile(file) {
  if (!file) return;

  try {
    const image = await loadImage(file);
    currentFile = file;

    dropTitle.textContent = "选择另一张图片";
    dropHint.textContent = `已选择：${file.name}`;

    convertImage(image);
  } catch (error) {
    showToast(error.message);
  }
}

fileInput.addEventListener("change", () => {
  processFile(fileInput.files[0]);

  // 清空文件值，后续可以再次选择同一张图片
  fileInput.value = "";
});

replaceButton.addEventListener("click", () => {
  fileInput.click();
});

function convertImage(image) {
  const width = Number(widthInput.value);
  const height = Math.max(
    1,
    Math.round((image.naturalHeight / image.naturalWidth) * width * 0.5),
  );

  canvas.width = width;
  canvas.height = height;

  const context = canvas.getContext("2d", { willReadFrequently: true });
  context.fillStyle = "#ffffff";
  context.fillRect(0, 0, width, height);
  context.drawImage(image, 0, 0, width, height);

  const pixels = context.getImageData(0, 0, width, height).data;
  const chars = charSet.value;
  const invert = invertInput.checked;
  const lines = [];

  for (let y = 0; y < height; y += 1) {
    let line = "";

    for (let x = 0; x < width; x += 1) {
      const offset = (y * width + x) * 4;
      let brightness =
        pixels[offset] * 0.299 +
        pixels[offset + 1] * 0.587 +
        pixels[offset + 2] * 0.114;

      if (invert) {
        brightness = 255 - brightness;
      }

      if (brightness > 240) {
        line += chars === "@%#*+=-:. " ? " " : chars[chars.length - 1];
      } else {
        const index = Math.round((brightness / 255) * (chars.length - 1));
        line += chars[index];
      }
    }

    lines.push(line.trimEnd());
  }

  while (lines.length && lines[0].length === 0) lines.shift();
  while (lines.length && lines[lines.length - 1].length === 0) lines.pop();

  currentAscii = lines.join("\n");
  asciiOutput.textContent = currentAscii;
  asciiOutput.hidden = false;
  emptyState.hidden = true;
  copyButton.disabled = false;
  downloadButton.disabled = false;
  sizeLabel.textContent = `${width} × ${lines.length} 字符`;
}

async function processFile(file) {
  if (!file) return;

  try {
    const image = await loadImage(file);
    currentFile = file;
    dropTitle.textContent = file.name;
    dropHint.textContent = `${(file.size / 1024).toFixed(1)} KB`;
    convertImage(image);
  } catch (error) {
    showToast(error.message);
  }
}

fileInput.addEventListener("change", () => {
  processFile(fileInput.files[0]);
});

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.add("dragging");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragging");
  });
});

dropZone.addEventListener("drop", (event) => {
  processFile(event.dataTransfer.files[0]);
});

widthInput.addEventListener("input", () => {
  widthOutput.textContent = `${widthInput.value} 字符`;
  if (currentFile) processFile(currentFile);
});

charSet.addEventListener("change", () => {
  if (currentFile) processFile(currentFile);
});

invertInput.addEventListener("change", () => {
  if (currentFile) processFile(currentFile);
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(currentAscii);
    showToast("已复制到剪贴板");
  } catch {
    const textarea = document.createElement("textarea");
    textarea.value = currentAscii;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
    showToast("已复制到剪贴板");
  }
});

downloadButton.addEventListener("click", () => {
  const blob = new Blob([currentAscii], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  const baseName = currentFile
    ? currentFile.name.replace(/\.[^.]+$/, "")
    : "ascii";

  link.href = url;
  link.download = `${baseName}-ascii.txt`;
  link.click();
  URL.revokeObjectURL(url);
  showToast("已生成文本文件");
});
