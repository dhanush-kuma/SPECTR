import { NavLink } from 'react-router-dom'
import { ORGANIZER_LABEL, INVESTIGATOR_LABEL } from '../labels'

function Header({ children }) {
  return (
    <header className="app-header">
      <div className="header-left">
        <NavLink to="/" className="site-name">
          Study Randomizer
        </NavLink>
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
      </div>
      {children}
    </header>
  )
}

export default Header
