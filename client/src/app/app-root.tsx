import { useState } from "react"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import "tidgrid"
import useSocketIO from "../hooks/use-socketio"
import IndexRoute from "../routes/index.route"
import "./index.sass"

function AppRoot() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isAuthenticationInProgress, setIsAuthenticationInProgress] = (
    useState(false)
  )
  const socketio = useSocketIO("http://localhost:8000/")

  function handleAuthenticationRequest() {
    socketio.emitEvent("authentication-request")
    setIsAuthenticationInProgress(true)
  }

  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={
            <IndexRoute
              isAuthenticated={isAuthenticated}
              isAuthenticationInProgress={isAuthenticationInProgress}
              handleAuthenticationRequest={handleAuthenticationRequest}
            />
          } />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default AppRoot
