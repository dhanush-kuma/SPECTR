import { NavLink } from 'react-router-dom'
import { ORGANIZER_LABEL, INVESTIGATOR_LABEL } from '../labels'

function Header({ children }) {
  return (
    <header className="app-header">
      <NavLink to="/" className="site-name">
        <span className="site-name__brand">SPECTR</span>
        <span className="site-name__tagline">
          <span className="site-name__by">by</span>
          <span className="site-name__org">MMMR</span>
        </span>
      </NavLink>
      <div className="header-right">
        <nav className="nav-menu">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Home
          </NavLink>
          <NavLink
            to="/admin"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Admin
          </NavLink>
          <NavLink
            to="/organizer"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Central Trial Coordinator (CTC)
          </NavLink>
          <NavLink
            to="/investigator"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Study Investigator (SI)
          </NavLink>
        </nav>
        {children}
      </div>
    </header>
  )
}

export default Header
