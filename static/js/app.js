document.addEventListener("DOMContentLoaded", () => {
    const generateButton = document.getElementById("generate-button");
    const questionInput = document.getElementById("question");
    const resultBox = document.getElementById("result");
    const buttonText = document.getElementById("button-text");
    const buttonIcon = document.getElementById("button-icon");
    const copyButton = document.getElementById("copy-button");

    console.log("EduGenie app.js loaded");

    if (!generateButton) {
        console.error("generate-button not found");
        return;
    }

    generateButton.addEventListener("click", async () => {
        const question = questionInput.value.trim();

        if (!question) {
            resultBox.innerText = "Please enter a question.";
            return;
        }

        generateButton.disabled = true;

        if (buttonIcon) {
            buttonIcon.innerText = "⏳";
        }

        if (buttonText) {
            buttonText.innerText = "Getting Answer...";
        }

        resultBox.className = "result-box";
        resultBox.innerText = "Thinking...";

        try {
            const response = await fetch("/qa", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            });

            const data = await response.json();

            console.log("API response:", data);

            if (!response.ok) {
                throw new Error(
                    data.detail || "Unable to get answer."
                );
            }

            const answer =
                data.answer ||
                data.response ||
                data.result ||
                JSON.stringify(data);

            resultBox.innerText = answer;

            if (copyButton) {
                copyButton.disabled = false;
            }

        } catch (error) {
            console.error("API Error:", error);

            resultBox.innerText =
                "Error: " + error.message;

        } finally {
            generateButton.disabled = false;

            if (buttonIcon) {
                buttonIcon.innerText = "✨";
            }

            if (buttonText) {
                buttonText.innerText = "Get Answer";
            }
        }
    });

    if (copyButton) {
        copyButton.addEventListener("click", async () => {
            try {
                await navigator.clipboard.writeText(
                    resultBox.innerText
                );

                copyButton.innerText = "Copied!";

                setTimeout(() => {
                    copyButton.innerText = "Copy";
                }, 1500);

            } catch (error) {
                console.error("Copy failed:", error);
            }
        });
    }
});