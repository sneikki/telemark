import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import AppRoot from "./app/app-root"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppRoot />
  </StrictMode>
)
