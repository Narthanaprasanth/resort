import React from 'react';
import { CONFIG } from '../config';

export function Header({ siteConfig }) {
  const words = CONFIG.RESORT_NAME.split(' ');
  const mono = words.map(w => w[0]).join('').slice(0, 3).toUpperCase();
  const lastWord = words.pop();
  const firstParts = words.join(' ');

  return (
    <header className="header">
      <div className="header-shimmer"></div>
      <div className="header-pattern"></div>
      <div className="header-inner">
        <div className="header-brand">
          {siteConfig?.logo ? (
            <img className='logo' src={siteConfig.logo} alt="Logo" style={{ borderRadius: '5px', height: '60px' }} />
          ) : (
            <div className="header-monogram">{mono}</div>
          )}
          <h1 className="header-title">Travel Agent Vendor Registration Form</h1>
        </div>
      </div>
      <div className="header-divider"></div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="footer">
      <p><span>{CONFIG.RESORT_NAME}</span> &nbsp;·&nbsp; Agent Partner Portal &nbsp;·&nbsp; Confidential &nbsp;·&nbsp; <span>{CONFIG.FOOTER_CREDIT}</span></p>
    </footer>
  );
}

export function ProgressNav({ currentStep, labels }) {
  return (
    <nav className="progress-nav" aria-label="Form steps">
      <div className="progress-track">
        {labels.map((lbl, i) => {
          const cls = i < currentStep ? 'done' : i === currentStep ? 'active' : '';
          const isLast = i === labels.length - 1;
          return (
            <React.Fragment key={i}>
              <div className={`pt-step ${cls}`}>
                <div className="pt-num">{i < currentStep ? '✓' : i + 1}</div>
                <div className="pt-label">{lbl}</div>
              </div>
              {!isLast && <div className="pt-line"></div>}
            </React.Fragment>
          );
        })}
      </div>
    </nav>
  );
}
