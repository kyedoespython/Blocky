const plans = [
  {
    id: 'free',
    label: 'Free tier',
    price: '£0',
    cadence: 'for 5 days',
    description: 'A focused introduction to the Blocky learning path.',
    features: ['Foundation SQL lessons', 'Basic roadmap access', 'Progress and points tracking'],
    action: 'Start free',
  },
  {
    id: 'standard',
    label: 'Standard',
    price: '£5.99',
    cadence: 'per month',
    description: 'More depth, more direction, and room to keep building.',
    features: ['Everything in Free', 'Advanced learning roadmaps', 'Expanded SQL exercises', 'Progress insights'],
    action: 'Choose Standard',
    featured: true,
  },
  {
    id: 'gold',
    label: 'Gold',
    price: '£10.99',
    cadence: 'per month',
    description: 'A complete private practice space for serious learners.',
    features: ['Everything in Standard', 'Advanced learning roadmaps', 'Isolated test environments', 'More project-based practice', 'Priority feature access'],
    action: 'Choose Gold',
  },
]

export default function Plans({ onBack, onOpenLearning, onOpenSettings }) {
  return (
    <main className="plans-page">
      <nav className="learning-nav">
        <button className="learning-brand" onClick={onBack} type="button">blocky<span>.</span></button>
        <div className="learning-nav-links">
          <button onClick={onOpenLearning} type="button">SQL path</button>
          <button onClick={onOpenSettings} type="button">Settings</button>
          <span className="active">Plans</span>
        </div>
      </nav>

      <header className="plans-header">
        <p className="content-kicker">Choose your pace</p>
        <h1>More room to<br /><em>learn deeply.</em></h1>
        <p>Start small, build momentum, and unlock the tools that match the way you want to learn.</p>
      </header>

      <section className="plan-grid" aria-label="Membership plans">
        {plans.map((plan) => (
          <article className={plan.featured ? 'plan-card featured' : 'plan-card'} key={plan.id}>
            {plan.featured && <span className="plan-badge">Most popular</span>}
            <div className="plan-card-top"><p className="plan-label">{plan.label}</p><span className="plan-index">0{plans.indexOf(plan) + 1}</span></div>
            <div className="plan-price"><strong>{plan.price}</strong><span>{plan.cadence}</span></div>
            <p className="plan-description">{plan.description}</p>
            <div className="plan-rule" />
            <ul>{plan.features.map((feature) => <li key={feature}><span>+</span>{feature}</li>)}</ul>
            <button className="plan-action" type="button">{plan.action}<span>-&gt;</span></button>
          </article>
        ))}
      </section>

      <p className="plans-note">Payments are not connected yet. Membership selection is currently a visual preview.</p>
      <footer className="site-footer"><span>Blocky</span><span>Learn at your own pace.</span><button onClick={onBack} type="button">Back home</button></footer>
    </main>
  )
}
