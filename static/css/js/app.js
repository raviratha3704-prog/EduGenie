// =========================================================
// EduGenie Frontend
// =========================================================


// ---------------------------------------------------------
// DOM elements
// ---------------------------------------------------------

const taskButtons =
    document.querySelectorAll(".task-button");

const mainInput =
    document.getElementById("main-input");

const inputLabel =
    document.getElementById("input-label");

const inputTitle =
    document.getElementById("input-title");

const generateButton =
    document.getElementById("generate-button");

const buttonText =
    document.getElementById("button-text");

const buttonIcon =
    document.getElementById("button-icon");

const resultBox =
    document.getElementById("result");

const copyButton =
    document.getElementById("copy-button");

const quizOptions =
    document.getElementById("quiz-options");

const quizTopic =
    document.getElementById("quiz-topic");

const learningOptions =
    document.getElementById("learning-options");

const learningLevel =
    document.getElementById("learning-level");

const learningHours =
    document.getElementById("learning-hours");


// ---------------------------------------------------------
// Current task
// ---------------------------------------------------------

let currentTask = "qa";


// ---------------------------------------------------------
// Task configuration
// ---------------------------------------------------------

const taskConfig = {

    qa: {

        label: "Your Question",

        title: "Ask EduGenie anything",

        placeholder:
            "Example: Explain how neural networks learn.",

        button:
            "Get Answer",

        icon:
            "✨"

    },

    explain: {

        label: "Concept",

        title: "Explain a difficult concept",

        placeholder:
            "Example: Explain quantum computing in simple terms.",

        button:
            "Explain Concept",

        icon:
            "🧠"

    },

    quiz: {

        label: "Study Material",

        title: "Generate a practice quiz",

        placeholder:
            "Paste your notes, textbook section, or study material here...",

        button:
            "Generate Quiz",

        icon:
            "📝"

    },

    summarize: {

        label: "Study Material",

        title: "Create a quick summary",

        placeholder:
            "Paste the text you want to summarize here...",

        button:
            "Summarize",

        icon:
            "📚"

    },

    learn: {

        label: "Learning Goal",

        title: "Build your learning path",

        placeholder:
            "Example: Learn Python programming from beginner to advanced.",

        button:
            "Create Learning Path",

        icon:
            "🗺️"

    }

};


// ---------------------------------------------------------
// Change task
// ---------------------------------------------------------

function selectTask(task) {

    currentTask = task;

    const config =
        taskConfig[task];

    inputLabel.textContent =
        config.label;

    inputTitle.textContent =
        config.title;

    mainInput.placeholder =
        config.placeholder;

    buttonText.textContent =
        config.button;

    buttonIcon.textContent =
        config.icon;


    // Quiz fields
    if (task === "quiz") {

        quizOptions.classList.remove(
            "hidden"
        );

    } else {

        quizOptions.classList.add(
            "hidden"
        );

    }


    // Learning fields
    if (task === "learn") {

        learningOptions.classList.remove(
            "hidden"
        );

    } else {

        learningOptions.classList.add(
            "hidden"
        );

    }


    // Reset result
    resetResult();
}


// ---------------------------------------------------------
// Reset result
// ---------------------------------------------------------

function resetResult() {

    resultBox.className =
        "result-box empty";

    resultBox.innerHTML = `

        <div class="empty-state">

            <div class="empty-icon">
                ${taskConfig[currentTask].icon}
            </div>

            <h4>
                Ready to help
            </h4>

            <p>
                Enter your content and
                run EduGenie.
            </p>

        </div>

    `;

    copyButton.disabled = true;

}


// ---------------------------------------------------------
// Task button events
// ---------------------------------------------------------

taskButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            taskButtons.forEach(
                item =>
                    item.classList.remove(
                        "active"
                    )
            );

            button.classList.add(
                "active"
            );

            selectTask(
                button.dataset.task
            );

        }
    );

});


// ---------------------------------------------------------
// Loading
// ---------------------------------------------------------

function setLoading(
    loading
) {

    generateButton.disabled =
        loading;

    if (loading) {

        buttonText.textContent =
            "Generating...";

        buttonIcon.textContent =
            "⏳";

        resultBox.className =
            "result-box";

        resultBox.innerHTML = `

            <div class="loading">

                <div class="spinner"></div>

                <span>
                    EduGenie is thinking...
                </span>

            </div>

        `;

    } else {

        const config =
            taskConfig[currentTask];

        buttonText.textContent =
            config.button;

        buttonIcon.textContent =
            config.icon;

    }

}


// ---------------------------------------------------------
// API request
// ---------------------------------------------------------

async function callAPI() {

    const text =
        mainInput.value.trim();


    if (!text) {

        showError(
            "Please enter some content first."
        );

        return;

    }


    setLoading(true);


    try {

        let endpoint;
        let payload;


        switch (currentTask) {

            case "qa":

                endpoint =
                    "/qa";

                payload = {
                    question: text
                };

                break;


            case "explain":

                endpoint =
                    "/explain";

                payload = {
                    topic: text
                };

                break;


            case "quiz":

                endpoint =
                    "/quiz";

                payload = {

                    text: text,

                    topic:
                        quizTopic.value.trim()
                        || null

                };

                break;


            case "summarize":

                endpoint =
                    "/summarize";

                payload = {
                    text: text
                };

                break;


            case "learn":

                endpoint =
                    "/learn/recommendations";

                payload = {

                    topic: text,

                    level:
                        learningLevel.value,

                    hours_per_week:
                        Number(
                            learningHours.value
                        )

                };

                break;


            default:

                throw new Error(
                    "Unknown task."
                );

        }


        const response =
            await fetch(
                endpoint,
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "The server returned an error."
            );

        }


        renderResult(data);

    }

    catch (error) {

        showError(
            error.message
            || "Something went wrong."
        );

    }

    finally {

        setLoading(false);

    }

}


// ---------------------------------------------------------
// Render result
// ---------------------------------------------------------

function renderResult(
    data
) {

    copyButton.disabled =
        false;


    resultBox.className =
        "result-box";


    // Quiz
    if (
        currentTask === "quiz"
        && data.quiz
    ) {

        renderQuiz(
            data.quiz
        );

        return;

    }


    let content = "";


    if (data.answer) {

        content =
            data.answer;

    }

    else if (data.summary) {

        content =
            data.summary;

    }

    else if (data.recommendations) {

        content =
            data.recommendations;

    }


    let providerHTML = "";


    if (data.provider) {

        providerHTML = `

            <span class="provider-label">

                Provider:
                ${escapeHTML(
                    data.provider
                )}

            </span>

        `;

    }


    resultBox.innerHTML = `

        ${providerHTML}

        <div class="response-content">

            ${escapeHTML(
                content
            )}

        </div>

    `;

}


// ---------------------------------------------------------
// Render quiz
// ---------------------------------------------------------

function renderQuiz(
    quiz
) {

    resultBox.innerHTML = "";

    quiz.forEach(
        (question, index) => {

            const questionElement =
                document.createElement(
                    "div"
                );

            questionElement.className =
                "quiz-question";


            const title =
                document.createElement(
                    "h4"
                );

            title.textContent =
                `${index + 1}. ${question.question}`;


            questionElement.appendChild(
                title
            );


            question.options.forEach(
                option => {

                    const button =
                        document.createElement(
                            "button"
                        );

                    button.className =
                        "quiz-option";

                    button.textContent =
                        option;


                    button.addEventListener(
                        "click",
                        () => {

                            const allOptions =
                                questionElement
                                .querySelectorAll(
                                    ".quiz-option"
                                );

                            allOptions.forEach(
                                item => {
                                    item.disabled =
                                        true;
                                }
                            );


                            if (
                                option ===
                                question.correct_answer
                            ) {

                                button.classList.add(
                                    "correct"
                                );

                                feedback.textContent =
                                    "Correct! 🎉";

                            } else {

                                button.classList.add(
                                    "incorrect"
                                );

                                feedback.textContent =
                                    `Incorrect. Correct answer: ${question.correct_answer}`;

                            }

                        }
                    );


                    questionElement.appendChild(
                        button
                    );

                }
            );


            const feedback =
                document.createElement(
                    "div"
                );

            feedback.className =
                "quiz-feedback";


            questionElement.appendChild(
                feedback
            );


            resultBox.appendChild(
                questionElement
            );

        }
    );

}


// ---------------------------------------------------------
// Error
// ---------------------------------------------------------

function showError(
    message
) {

    resultBox.className =
        "result-box";

    resultBox.innerHTML = `

        <div class="error-message">

            <strong>
                Something went wrong
            </strong>

            <br><br>

            ${escapeHTML(message)}

        </div>

    `;

    copyButton.disabled =
        true;

}


// ---------------------------------------------------------
// Copy result
// ---------------------------------------------------------

copyButton.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                resultBox.innerText
            );

            const original =
                copyButton.textContent;

            copyButton.textContent =
                "Copied!";

            setTimeout(
                () => {

                    copyButton.textContent =
                        original;

                },
                1500
            );

        }

        catch {

            copyButton.textContent =
                "Copy failed";

        }

    }
);


// ---------------------------------------------------------
// HTML escaping
// ---------------------------------------------------------

function escapeHTML(
    value
) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

}


// ---------------------------------------------------------
// Keyboard shortcut
// ---------------------------------------------------------

mainInput.addEventListener(
    "keydown",
    event => {

        if (
            event.ctrlKey
            && event.key === "Enter"
        ) {

            callAPI();

        }

    }
);


// ---------------------------------------------------------
// Initial state
// ---------------------------------------------------------

selectTask("qa");