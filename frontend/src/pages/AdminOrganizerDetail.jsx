import { useEffect, useState } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { apiFetch } from '../api'
import Header from '../components/Header'
import {
  ORGANIZER_LABEL,
  INVESTIGATOR_LABEL_PLURAL,
  PARTICIPANT_LABEL_PLURAL,
} from '../labels'

const ORGANIZER_STATUS_LABELS = {
  active: { label: 'Active', cls: 'badge--active' },
  inactive: { label: 'Inactive', cls: 'badge--inactive' },
  disabled: { label: 'Disabled', cls: 'badge--disabled' },
}

function formatDate(value) {
  if (!value) return '—'
  return new Date(value).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

function StatCard({ label, value }) {
  return (
    <div className="status-card" style={{ maxWidth: 'none', margin: 0 }}>
      <div className="label">{label}</div>
      <div style={{ fontSize: '24px', fontWeight: 600, color: '#1a1a2e', marginTop: '4px' }}>
        {value}
      </div>
    </div>
  )
}

function AdminOrganizerDetail() {
  const { organizerId } = useParams()
  const navigate = useNavigate()
  const [organizer, setOrganizer] = useState(null)
  const [studies, setStudies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    setLoading(true)
    setError(null)

    Promise.all([
      apiFetch(`/admin/organizers/${organizerId}`),
      apiFetch(`/admin/organizers/${organizerId}/studies`),
    ])
      .then(async ([detailRes, studiesRes]) => {
        if (!detailRes.ok) {
          if (detailRes.status === 404) {
            navigate('/admin/home', { replace: true })
            return
          }
          throw new Error('Failed to load CTC details.')
        }
        const detail = await detailRes.json()
        const studyList = studiesRes.ok ? await studiesRes.json() : []
        setOrganizer(detail)
        setStudies(studyList)
      })
      .catch((err) => {
        setError(err.message || 'Could not load CTC details.')
      })
      .finally(() => setLoading(false))
  }, [organizerId, navigate])

  const status = organizer
    ? ORGANIZER_STATUS_LABELS[organizer.status] || {
        label: organizer.status,
        cls: 'badge--inactive',
      }
    : null

  return (
    <>
      <Header>
        <Link to="/admin/home" className="btn-secondary" style={{ textDecoration: 'none' }}>
          ← Back to Admin
        </Link>
      </Header>

      <main className="app">
        {loading ? (
          <p className="loading">Loading…</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : organizer ? (
          <>
            <div className="section-header" style={{ marginBottom: '20px' }}>
              <div>
                <h1 style={{ marginBottom: '6px' }}>{ORGANIZER_LABEL} Usage</h1>
                <p style={{ color: '#555', fontSize: '14px', margin: 0 }}>
                  {organizer.username}
                  {status && (
                    <span className={`badge ${status.cls}`} style={{ marginLeft: '10px' }}>
                      {status.label}
                    </span>
                  )}
                </p>
              </div>
            </div>

            <div className="status-card" style={{ marginBottom: '24px' }}>
              <div className="label">Account</div>
              <p className="message" style={{ margin: '4px 0 0' }}>
                Joined <strong>{formatDate(organizer.created_at)}</strong>
                {organizer.terms_accepted_at && (
                  <>
                    {' · '}
                    ToS accepted <strong>{formatDate(organizer.terms_accepted_at)}</strong>
                  </>
                )}
              </p>
            </div>

            <h2 className="section-title" style={{ marginBottom: '12px' }}>Resource Usage</h2>
            <div className="stats-grid" style={{ marginBottom: '28px' }}>
              <StatCard label="Studies" value={organizer.study_count} />
              <StatCard label="Active Studies" value={organizer.active_study_count} />
              <StatCard label="Sites" value={organizer.site_count} />
              <StatCard label={INVESTIGATOR_LABEL_PLURAL} value={organizer.investigator_count} />
              <StatCard label="Randomization Kits" value={organizer.total_randomization_records} />
              <StatCard
                label={`Assigned ${PARTICIPANT_LABEL_PLURAL}`}
                value={organizer.assigned_participants}
              />
            </div>

            <div className="section-header">
              <h2 className="section-title">Studies</h2>
            </div>

            {studies.length === 0 ? (
              <p className="empty-state">No studies created by this {ORGANIZER_LABEL} yet.</p>
            ) : (
              <div className="table-scroll">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Protocol Code</th>
                      <th>Title</th>
                      <th>Status</th>
                      <th>Sites</th>
                      <th>{INVESTIGATOR_LABEL_PLURAL}</th>
                      <th>Kits</th>
                      <th>Assigned</th>
                      <th>Unassigned</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {studies.map((study) => (
                      <tr key={study.id}>
                        <td>{study.id}</td>
                        <td><strong>{study.protocol_code}</strong></td>
                        <td>{study.title}</td>
                        <td>
                          <span
                            className={`badge badge--${
                              study.status === 'Draft' ? 'inactive' : 'active'
                            }`}
                          >
                            {study.status}
                          </span>
                        </td>
                        <td>{study.site_count}</td>
                        <td>{study.investigator_count}</td>
                        <td>{study.total_records}</td>
                        <td>{study.assigned}</td>
                        <td>{study.unassigned}</td>
                        <td>{formatDate(study.created_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </>
        ) : null}
      </main>
    </>
  )
}

export default AdminOrganizerDetail
