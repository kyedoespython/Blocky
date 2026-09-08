import { useEffect, useState } from 'react'
import { completeLesson, getProgress } from './api'

const lessons = [
  {
    id: 'select',
    label: 'SELECT basics',
    level: '01',
    title: 'Ask your database a question.',
    copy: 'SQL becomes useful when you can turn a question into a precise request for data.',
    query: 'SELECT name, role\nFROM learners\nWHERE active = true;',
    result: ['Alex Morgan | Student', 'Priya Shah | Developer', 'Jordan Lee | Student'],
  },
  {
    id: 'where',
    label: 'Filtering with WHERE',
    level: '02',
    title: 'Keep only what matters.',
    copy: 'Use conditions to narrow a result set. Start with one condition, then combine them carefully.',
    query: "SELECT *\nFROM courses\nWHERE difficulty = 'beginner';",
    result: ['SQL foundations | beginner', 'Tables and relationships | beginner'],
  },
  {
    id: 'join',
    label: 'Connecting tables',
    level: '03',
    title: 'Bring related data together.',
    copy: 'Joins connect rows that belong together through a shared key.',
    query: 'SELECT learners.name, courses.title\nFROM learners\nJOIN enrollments ON learners.id = enrollments.learner_id\nJOIN courses ON courses.id = enrollments.course_id;',
    result: ['Alex Morgan | SQL foundations', 'Priya Shah | Query performance'],
  },
  {
    id: 'group',
    label: 'GROUP BY',
    level: '04',
    title: 'Find patterns in a crowd.',
    copy: 'Aggregation turns many rows into a useful summary, such as a count per course.',
    query: 'SELECT course_id, COUNT(*) AS learner_count\nFROM enrollments\nGROUP BY course_id;',
    result: ['SQL foundations | 42 learners', 'Data modeling | 18 learners'],
  },
]

function PostgreSQLGuide() {
  return (
    <section className="postgres-guide">
      <p className="content-kicker">Set up your own database</p>
      <h3>PostgreSQL on Windows x64</h3>
      <p>Use this short path to get a local PostgreSQL server ready for practice.</p>
      <ol>
        <li><strong>Download the x64 installer.</strong> Use the official PostgreSQL Windows installer from EDB and choose a supported release.</li>
        <li><strong>Install the essentials.</strong> Keep PostgreSQL Server, pgAdmin, and Command Line Tools selected.</li>
        <li><strong>Choose a password.</strong> Save the password for the <code>postgres</code> role in a password manager. Never put it in frontend code.</li>
        <li><strong>Keep the defaults.</strong> Port <code>5432</code> is a sensible local default. Add the PostgreSQL <code>bin</code> folder to PATH if you want to use <code>psql</code> anywhere.</li>
        <li><strong>Verify the install.</strong> Open PowerShell and run <code>psql --version</code>, then connect with <code>psql -U postgres</code>.</li>
        <li><strong>Create a practice database.</strong> In psql, run <code>CREATE DATABASE blocky_lab;</code>. Use a separate local role for applications instead of the superuser.</li>
      </ol>
      <a href="https://www.postgresql.org/download/windows/" target="_blank" rel="noreferrer">Open the official Windows download page -&gt;</a>
    </section>
  )
}

export default function SQLLearning({ user, onUserChange, onOpenSettings, onOpenPlans, onBack }) {
  const [activeId, setActiveId] = useState('select')
  const [completedLessons, setCompletedLessons] = useState([])
  const [completionMessage, setCompletionMessage] = useState('')
  const [isCelebrating, setIsCelebrating] = useState(false)

  useEffect(() => {
    if (user) getProgress().then((response) => setCompletedLessons(response.lessons_completed)).catch(() => {})
  }, [user])
  const activeLesson = lessons.find((lesson) => lesson.id === activeId)
  const activeIndex = lessons.findIndex((lesson) => lesson.id === activeId)
  const nextLesson = lessons[(activeIndex + 1) % lessons.length]

  async function markComplete() {
    if (!user) {
      setCompletionMessage('Log in to save lesson progress.')
      return
    }
    try {
      const response = await completeLesson(activeId)
      setCompletedLessons((current) => current.includes(activeId) ? current : [...current, activeId])
      onUserChange({ ...user, points: response.points, lessons_completed: response.lessons_completed })
      setCompletionMessage(response.awarded ? '+1 point. Lesson complete.' : 'Already completed.')
      setIsCelebrating(true)
      window.setTimeout(() => setIsCelebrating(false), 650)
    } catch (requestError) {
      setCompletionMessage(requestError.message)
    }
  }

  return (
    <main className="learning-page">
      <nav className="learning-nav">
        <button className="learning-brand" onClick={onBack} type="button">blocky<span>.</span></button>
        <div className="learning-nav-links"><span className="active">SQL path</span>{user && <button onClick={onOpenSettings} type="button">Settings</button>}<button onClick={onOpenPlans} type="button">Plans</button><button onClick={onBack} type="button">Exit lesson</button></div>
      </nav>

      <div className="learning-layout">
        <aside className="lesson-rail" aria-label="SQL lessons">
          <p className="rail-kicker">SQL / foundations</p>
          <h1>Learn by<br /><em>querying.</em></h1>
          <p className="rail-copy">Short lessons. Real questions. A place to make mistakes safely.</p>
          <div className="progress-line"><span style={{ width: `${Math.max(8, (completedLessons.length / lessons.length) * 100)}%` }} /></div>
          <p className="progress-label">{completedLessons.length} of {lessons.length} lessons complete · {user?.points || 0} points</p>
          <div className="lesson-list">
            {lessons.map((lesson) => (
              <button className={`${lesson.id === activeId ? 'lesson active' : 'lesson'} ${completedLessons.includes(lesson.id) ? 'complete' : ''}`} key={lesson.id} onClick={() => setActiveId(lesson.id)} type="button">
                <span>{lesson.level}</span>{lesson.label}<b>{completedLessons.includes(lesson.id) ? 'done' : lesson.id === activeId ? 'current' : ''}</b>
              </button>
            ))}
          </div>
        </aside>

        <section className="lesson-content">
          <div className="lesson-heading">
            <p className="content-kicker">Lesson {activeLesson.level}</p>
            <h2>{activeLesson.title}</h2>
            <p>{activeLesson.copy}</p>
          </div>

          <div className={isCelebrating ? 'query-workbench lesson-celebration' : 'query-workbench'}>
            <div className="workbench-top"><span><i /> live example</span><span>read only</span></div>
            <pre><code>{activeLesson.query}</code></pre>
            <div className="result-heading"><span>Result preview</span><span>{activeLesson.result.length} rows</span></div>
            <div className="result-rows">{activeLesson.result.map((row) => <div key={row}><span className="row-dot" />{row}</div>)}</div>
          </div>

          <div className="lesson-foot">
            <div><span className="tip-icon">Tip</span><p><strong>Think about it</strong><br />What would change if you removed the condition?</p></div>
            <div className="lesson-actions"><button className="complete-button" onClick={markComplete} type="button">{completedLessons.includes(activeId) ? 'Completed' : 'Complete lesson'}</button><button className="next-button" onClick={() => setActiveId(nextLesson.id)} type="button">Next concept <span>-&gt;</span></button></div>
          </div>
          {completionMessage && <p className="completion-message" role="status">{completionMessage}</p>}
          <PostgreSQLGuide />
        </section>
      </div>
    </main>
  )
}
