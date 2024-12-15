import { type SocketIO } from "../hooks/use-socketio"
import PageHeader from "../components/page-header"
import "./index.route.sass"

export interface IndexRouteProps {
  isAuthenticated: boolean
  isAuthenticationInProgress: boolean
  handleAuthenticationRequest(): void
}

function IndexRoute(props: IndexRouteProps) {
  const {
    isAuthenticated,
    isAuthenticationInProgress,
    handleAuthenticationRequest
  } = props

  console.log(isAuthenticationInProgress)

  return (
    <main>
      <PageHeader />

      <section className="tg-section">
        <div className="tg-container(lg)">
          <div className="tg-row tg-y-gap(md)">
            <div className="tg-cell">
              <p className="index-route-jumbo-text index-route-jumbo-text-large">Welcome to Telemark!</p>
            </div>
            <div className="tg-cell">
              <p className="index-route-jumbo-text">Click the button below to authenticate:</p>
            </div>
          </div>
        </div>
      </section>

      <section className="tg-section">
        <div className="tg-container(lg)">
          <div className="tg-row tg-mode(thin) tg-pos-x(center)">
            <div className="tg-cell">
              <button
                disabled={isAuthenticationInProgress}
                onClick={handleAuthenticationRequest}
                className="telemark-button telemark-button-inverted telemark-button-large"
              >
                Authenticate
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}

export default IndexRoute
