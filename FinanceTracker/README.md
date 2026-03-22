# WealthAI - Full-Stack Finance Tracker

An AI-powered financial tracking application built with the MERN stack, featuring a premium dark-themed UI inspired by Stitch.

## Features

- **Personalized Dashboard**: Real-time tracking of balances, spending, and ROI.
- **AI Insights**: Automated analysis of spending patterns with smart recommendations.
- **Transaction Management**: Categorized transaction history.
- **Secure Authentication**: JWT-based user login and registration.
- **Premium UI**: Modern dark mode interface with glassmorphism and responsive design.

## Tech Stack

- **Frontend**: React (Vite), Tailwind CSS, Lucide React, Framer Motion.
- **Backend**: Node.js, Express.js.
- **Database**: MongoDB (Mongoose).
- **Authentication**: JWT, Bcrypt.js.

## Getting Started (Local Development)

### Prerequisites

- Node.js installed on your machine.
- MongoDB running locally (default: `mongodb://localhost:27017/financeTracker`).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd FinanceTracker
    ```

2.  **Setup Backend**
    ```bash
    # Open a terminal in the root folder
    npm install
    # Verify server/.env configuration
    ```

3.  **Setup Frontend**
    ```bash
    cd client
    npm install
    ```

### Running the App

1.  **Start the Backend Server**
    ```bash
    # From the root directory
    node server/server.js
    ```

2.  **Start the Frontend Development Server**
    ```bash
    # From the client directory
    npm run dev
    ```

3.  **Access the Website**
    Open [http://localhost:5173](http://localhost:5173) in your browser.

## Project Structure

- `server/`: Express backend with MongoDB models and routes.
- `client/`: React frontend with components and pages.
- `client/src/pages/`: Main application views (Dashboard, Insights, Landing).
- `client/src/components/`: Reusable UI elements.

## License

This project is licensed under the MIT License.
