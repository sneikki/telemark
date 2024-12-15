import { FaBars } from "react-icons/fa6"
import "./page-header.sass"

function PageHeader() {
  return (
      <header className="tg-section">
        <div className="tg-container(lg)">
          <div className="tg-row tg-mode(thin) tg-pos-y(center) tg-space-x(between)">
            <div className="tg-cell">
              <p className="page-header-logo">Telemark</p>
            </div>

            <div className="tg-cell">
              <FaBars size={32} color="#080808" />
            </div>
          </div>
        </div>
      </header>
  )
}

export default PageHeader
