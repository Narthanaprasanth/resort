import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { CONFIG } from './config';
import { Header, Footer, ProgressNav } from './components/Layout';
import {
  Step0Agency,
  Step1Contact,
  Step2Business,
  Step3Partnership,
  Step4Banking,
  Step5Terms,
  Step6Review,
  StepSuccess
} from './components/FormSteps';

function shadeColor(hex, pct) {
  const num = parseInt(hex.replace('#',''), 16);
  const r = Math.min(255, Math.max(0, (num>>16) + pct*2));
  const g = Math.min(255, Math.max(0, ((num>>8)&0xff) + pct*2));
  const b = Math.min(255, Math.max(0, (num&0xff) + pct*2));
  return '#' + [r,g,b].map(x => x.toString(16).padStart(2,'0')).join('');
}

function hexToRgba(hex, a) {
  const num = parseInt(hex.replace('#',''), 16);
  return `rgba(${num>>16},${(num>>8)&0xff},${num&0xff},${a})`;
}

const STEP_LABELS = ['Agency','Contact','Business','Partnership','Banking','Terms','Review'];

const initialData = {
  agency_name: '', year_established: '', website: '', company_type: '', primary_market: '',
  contact_name: '', contact_designation: '', contact_mobile: '', contact_email: '', address: '', city: '', pin: '',
  top_destinations: '', avg_monthly_bookings: '', client_types: [],
  expected_monthly_room_nights: '', preferred_room_category: '', commission_requested: '', preferred_payment_terms: '',
  bank_name: '', account_name: '', account_number: '', ifsc_code: '',
  docs_gst: null, docs_pan: null, docs_company: null, docs_cheque: null,
  agreed: false, signatory_name: '', signatory_designation: '', signatory_date: ''
};

export default function App() {
  const [currentStep, setCurrentStep] = useState(0);
  const [data, setData] = useState(initialData);
  const [isSuccess, setIsSuccess] = useState(false);
  const [vendorId, setVendorId] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [siteConfig, setSiteConfig] = useState(null);

  useEffect(() => {
    // Fetch site config (logo + header color)
    axios.get('/api/config/')
      .then(res => {
        setSiteConfig(res.data);
        if (res.data.header_bg_color) {
          document.documentElement.style.setProperty('--header-bg', res.data.header_bg_color);
        }
      })
      .catch(err => console.error('Failed to fetch config:', err));

    document.title = `${CONFIG.RESORT_NAME} — Agent Registration`;
    document.documentElement.style.setProperty('--primary', CONFIG.COLOR_PRIMARY);
    document.documentElement.style.setProperty('--primary-dark', shadeColor(CONFIG.COLOR_PRIMARY, -25));
    document.documentElement.style.setProperty('--primary-mid', shadeColor(CONFIG.COLOR_PRIMARY, 15));
    document.documentElement.style.setProperty('--accent', CONFIG.COLOR_ACCENT);
    document.documentElement.style.setProperty('--accent-light', shadeColor(CONFIG.COLOR_ACCENT, 15));
    document.documentElement.style.setProperty('--accent-pale', CONFIG.COLOR_LIGHT);
    document.documentElement.style.setProperty('--accent-dim', hexToRgba(CONFIG.COLOR_ACCENT, 0.1));
  }, []);

  const nextStep = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setCurrentStep(prev => prev + 1);
  };
  
  const prevStep = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setCurrentStep(prev => prev - 1);
  };

  const submitForm = async () => {
    setIsSubmitting(true);
    try {
      const formData = new FormData();
      for (const key in data) {
        if (data[key] !== null) {
          if (Array.isArray(data[key])) {
            // Send arrays as JSON string so DRF JSONField parses it correctly
            formData.append(key, JSON.stringify(data[key]));
          } else {
            formData.append(key, data[key]);
          }
        }
      }

      const response = await axios.post('/api/registrations/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setVendorId(response.data.vendor_id);
      setIsSuccess(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
      console.error("Error submitting form:", error);
      if (error.response?.data) {
        // Show field-level validation errors from Django
        const errs = error.response.data;
        const msg = Object.entries(errs)
          .map(([field, messages]) => `• ${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
          .join('\n');
        alert(`Submission failed. Please fix the following:\n\n${msg}`);
      } else {
        alert("There was an error submitting the form. Please try again.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStep = () => {
    if (isSuccess) return <StepSuccess data={data} vendorId={vendorId} config={CONFIG} />;
    switch (currentStep) {
      case 0: return <Step0Agency data={data} setData={setData} />;
      case 1: return <Step1Contact data={data} setData={setData} />;
      case 2: return <Step2Business data={data} setData={setData} />;
      case 3: return <Step3Partnership data={data} setData={setData} />;
      case 4: return <Step4Banking data={data} setData={setData} />;
      case 5: return <Step5Terms data={data} setData={setData} />;
      case 6: return <Step6Review data={data} />;
      default: return null;
    }
  };

  return (
    <>
      <Header siteConfig={siteConfig} />
      {!isSuccess && <ProgressNav currentStep={currentStep} labels={STEP_LABELS} />}
      
      <main className="main">
        {renderStep()}

        {!isSuccess && (
          <div id="form-nav" className="nav-row" style={{ display: 'flex' }}>
            <button className="btn-back" onClick={prevStep} disabled={currentStep === 0 || isSubmitting}>
              ← Back
            </button>
            <span className="step-counter">Step <strong>{currentStep + 1}</strong> of {STEP_LABELS.length}</span>
            {currentStep === STEP_LABELS.length - 1 ? (
              <button className="btn-submit" onClick={submitForm} disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit Registration →'}
              </button>
            ) : (
              <button className="btn-next" onClick={nextStep}>
                Continue →
              </button>
            )}
          </div>
        )}
      </main>

      <Footer />
    </>
  );
}
