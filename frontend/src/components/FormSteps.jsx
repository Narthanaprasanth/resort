import React from 'react';

function CheckboxPill({ label, checked, onChange }) {
  return (
    <div className={`cb-pill ${checked ? 'on' : ''}`} onClick={onChange}>
      <div className="cb-dot"></div>{label}
    </div>
  );
}

export function Step0Agency({ data, setData }) {
  const toggleCompany = (val) => setData({ ...data, company_type: val });
  const toggleMarket = (val) => setData({ ...data, primary_market: val });

  return (
    <div className="step-panel active">
      <div className="card">
        <div className="card-title">1. Agency Details</div>
        <div className="fg c2">
          <div className="f"><label>Agency Name <span className="r">*</span></label><input type="text" value={data.agency_name} onChange={e => setData({ ...data, agency_name: e.target.value })} placeholder="Registered agency name" /></div>
          <div className="f"><label>Year Established <span className="r">*</span></label><input type="text" value={data.year_established} onChange={e => setData({ ...data, year_established: e.target.value })} placeholder="e.g. 2012" /></div>
        </div>
        <div className="mt">
          <div className="f"><label>Company Type <span className="r">*</span></label></div>
          <div className="cb-group">
            {['Individual', 'Partnership', 'Pvt Ltd', 'LLP', 'Other'].map(type => (
              <CheckboxPill key={type} label={type} checked={data.company_type === type} onChange={() => toggleCompany(type)} />
            ))}
          </div>
        </div>
        <div className="mt">
          <div className="f"><label>Primary Market <span className="r">*</span></label></div>
          <div className="cb-group">
            {['Domestic', 'International', 'Both'].map(type => (
              <CheckboxPill key={type} label={type} checked={data.primary_market === type} onChange={() => toggleMarket(type)} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export function Step1Contact({ data, setData }) {
  return (
    <div className="step-panel active">
      <div className="card">
        <div className="card-title">2. Contact Person Details</div>
        <div className="fg c2">
          <div className="f"><label>Name <span className="r">*</span></label><input type="text" value={data.contact_name} onChange={e => setData({ ...data, contact_name: e.target.value })} /></div>
          <div className="f"><label>Designation <span className="r">*</span></label><input type="text" value={data.contact_designation} onChange={e => setData({ ...data, contact_designation: e.target.value })} placeholder="e.g. Director, Manager" /></div>
        </div>
        <div className="fg c2 mt">
          <div className="f"><label>Mobile Number <span className="r">*</span></label><input type="tel" value={data.contact_mobile} onChange={e => setData({ ...data, contact_mobile: e.target.value })} placeholder="+91" /></div>
          <div className="f"><label>Email Address <span className="r">*</span></label><input type="email" value={data.contact_email} onChange={e => setData({ ...data, contact_email: e.target.value })} /></div>
        </div>
      </div>
      <div className="card">
        <div className="card-title">3. Office Address</div>
        <div className="f">
          <label>Registered Address <span className="r">*</span></label>
          <textarea value={data.address} onChange={e => setData({ ...data, address: e.target.value })} placeholder="Street, area, landmark..."></textarea>
        </div>
        <div className="fg c2 mt">
          <div className="f"><label>City / State / Country <span className="r">*</span></label><input type="text" value={data.city} onChange={e => setData({ ...data, city: e.target.value })} /></div>
          <div className="f"><label>Website</label><input type="url" value={data.website} onChange={e => setData({ ...data, website: e.target.value })} placeholder="https://youragency.com" /></div>
        </div>
      </div>
    </div>
  );
}

export function Step2Business({ data, setData }) {
  const toggleClient = (type) => {
    const clients = [...data.client_types];
    if (clients.includes(type)) {
      setData({ ...data, client_types: clients.filter(c => c !== type) });
    } else {
      setData({ ...data, client_types: [...clients, type] });
    }
  };

  return (
    <div className="step-panel active">
      <div className="card">
        <div className="card-title">4. Business Profile</div>
        <div className="fg c2">
          <div className="f"><label>Top Destinations Sold <span className="r">*</span></label><input type="text" value={data.top_destinations} onChange={e => setData({ ...data, top_destinations: e.target.value })} placeholder="e.g. Ooty, Munnar, Coorg" /></div>
          <div className="f"><label>Average Monthly Bookings <span className="r">*</span></label><input type="text" value={data.avg_monthly_bookings} onChange={e => setData({ ...data, avg_monthly_bookings: e.target.value })} placeholder="e.g. 40–60 pax" /></div>
        </div>
        <div className="mt">
          <div className="f"><label>Client Type <span className="r">*</span></label></div>
          <div className="cb-group">
            {['FIT', 'Groups', 'Corporate', 'MICE', 'Mixed'].map(type => (
              <CheckboxPill key={type} label={type} checked={data.client_types.includes(type)} onChange={() => toggleClient(type)} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export function Step3Partnership({ data, setData }) {
  return (
    <div className="step-panel active">
      <div className="card">
        <div className="card-title">5. Partnership Expectations</div>
        <div className="fg c2">
          <div className="f"><label>Expected Monthly Room Nights <span className="r">*</span></label><input type="text" value={data.expected_monthly_room_nights} onChange={e => setData({ ...data, expected_monthly_room_nights: e.target.value })} placeholder="e.g. 30" /></div>
          <div className="f"><label>Preferred Room Category</label><input type="text" value={data.preferred_room_category} onChange={e => setData({ ...data, preferred_room_category: e.target.value })} placeholder="e.g. Deluxe, Pool Suite" /></div>
        </div>
        <div className="fg c2 mt">
          <div className="f"><label>Commission Requested (%) <span className="r">*</span></label><input type="text" value={data.commission_requested} onChange={e => setData({ ...data, commission_requested: e.target.value })} placeholder="e.g. 10%" /></div>
          <div className="f"><label>Preferred Payment Terms <span className="r">*</span></label><input type="text" value={data.preferred_payment_terms} onChange={e => setData({ ...data, preferred_payment_terms: e.target.value })} placeholder="e.g. Net 15, Advance" /></div>
        </div>
      </div>
    </div>
  );
}

export function Step4Banking({ data, setData }) {
  const handleFile = (e, field) => {
    setData({ ...data, [field]: e.target.files[0] });
  };

  return (
    <div className="step-panel active">
      <div className="card">
        <div className="card-title">6. Banking Details</div>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '18px', lineHeight: 1.6 }}>For commission disbursements only. Information is kept strictly confidential.</p>
        <div className="fg c2">
          <div className="f"><label>Bank Name <span className="r">*</span></label><input type="text" value={data.bank_name} onChange={e => setData({ ...data, bank_name: e.target.value })} /></div>
          <div className="f"><label>Account Name <span className="r">*</span></label><input type="text" value={data.account_name} onChange={e => setData({ ...data, account_name: e.target.value })} /></div>
        </div>
        <div className="fg c2 mt">
          <div className="f"><label>Account Number <span className="r">*</span></label><input type="text" value={data.account_number} onChange={e => setData({ ...data, account_number: e.target.value })} /></div>
          <div className="f"><label>IFSC / SWIFT Code <span className="r">*</span></label><input type="text" value={data.ifsc_code} onChange={e => setData({ ...data, ifsc_code: e.target.value })} /></div>
        </div>
      </div>
      <div className="card">
        <div className="card-title">7. Documents Required (Attach Copies)</div>
        <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '14px' }}>Please attach self-attested copies of the following documents:</p>
        
        <div className="doc-grid" style={{ gridTemplateColumns: '1fr', gap: '16px' }}>
          <div className="f">
            <label>GST Registration</label>
            <input type="file" onChange={e => handleFile(e, 'docs_gst')} accept=".pdf,.jpg,.jpeg,.png" style={{ border: '1px solid var(--border)', padding: '10px', borderRadius: '5px' }} />
            {data.docs_gst && <div style={{ fontSize: '12px', color: 'green', marginTop: '4px' }}>✓ File attached: {data.docs_gst.name}</div>}
          </div>
          <div className="f">
            <label>PAN Card</label>
            <input type="file" onChange={e => handleFile(e, 'docs_pan')} accept=".pdf,.jpg,.jpeg,.png" style={{ border: '1px solid var(--border)', padding: '10px', borderRadius: '5px' }} />
            {data.docs_pan && <div style={{ fontSize: '12px', color: 'green', marginTop: '4px' }}>✓ File attached: {data.docs_pan.name}</div>}
          </div>
          <div className="f">
            <label>Company Registration Certificate</label>
            <input type="file" onChange={e => handleFile(e, 'docs_company')} accept=".pdf,.jpg,.jpeg,.png" style={{ border: '1px solid var(--border)', padding: '10px', borderRadius: '5px' }} />
            {data.docs_company && <div style={{ fontSize: '12px', color: 'green', marginTop: '4px' }}>✓ File attached: {data.docs_company.name}</div>}
          </div>
          <div className="f">
            <label>Cancelled Cheque</label>
            <input type="file" onChange={e => handleFile(e, 'docs_cheque')} accept=".pdf,.jpg,.jpeg,.png" style={{ border: '1px solid var(--border)', padding: '10px', borderRadius: '5px' }} />
            {data.docs_cheque && <div style={{ fontSize: '12px', color: 'green', marginTop: '4px' }}>✓ File attached: {data.docs_cheque.name}</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

export function Step5Terms({ data, setData }) {
  return (
    <div className="step-panel active">
      <div className="tc-dark">
        <div className="tc-dark-title">8. Terms & Conditions</div>
        <ul className="tc-list">
          <li>All bookings must be confirmed via official email communication only.</li>
          <li>Commission is applicable only on net room revenue, excluding all applicable taxes.</li>
          <li>Rate sheets are strictly confidential — not for public distribution or third parties.</li>
          <li>Payment terms agreed upon registration must be strictly adhered to.</li>
          <li>Cancellations and amendments are subject to the resort's prevailing cancellation policy.</li>
          <li>Rate undercutting of any form may result in immediate termination of partnership.</li>
        </ul>
      </div>
      <div className="card">
        <div className="card-title">9. Declaration</div>
        <div className={`agree-row ${data.agreed ? 'on' : ''}`} onClick={() => setData({ ...data, agreed: !data.agreed })}>
          <div className="agree-chk-box"><svg className="agree-icon" viewBox="0 0 12 12"><path d="M2,6 L5,9 L10,3" /></svg></div>
          <div className="agree-label">I hereby confirm that the above information is true and agree to comply with Sandalo Castle Resort policies.</div>
        </div>
        <div className="sig-row">
          <div className="sig-f"><label>Authorized Signatory <span className="r" style={{ color: 'var(--accent)' }}>*</span></label><input type="text" value={data.signatory_name} onChange={e => setData({ ...data, signatory_name: e.target.value })} /></div>
          <div className="sig-f"><label>Name <span className="r" style={{ color: 'var(--accent)' }}>*</span></label><input type="text" value={data.signatory_designation} onChange={e => setData({ ...data, signatory_designation: e.target.value })} /></div>
        </div>
        <div className="sig-row" style={{ marginTop: 0 }}>
          <div className="sig-f"><label>Date <span className="r" style={{ color: 'var(--accent)' }}>*</span></label><input type="date" value={data.signatory_date} onChange={e => setData({ ...data, signatory_date: e.target.value })} /></div>
          <div className="sig-f"></div>
        </div>
      </div>
    </div>
  );
}

export function Step6Review({ data }) {
  return (
    <div className="step-panel active">
      <div className="review-block">
        <div className="review-block-hd">Agency & Contact</div>
        <table className="review-tbl">
          <tbody>
            <tr><td>Agency Name</td><td>{data.agency_name || '—'}</td></tr>
            <tr><td>Company Type</td><td>{data.company_type || '—'}</td></tr>
            <tr><td>Year Est.</td><td>{data.year_established || '—'}</td></tr>
            <tr><td>Primary Market</td><td>{data.primary_market || '—'}</td></tr>
            <tr><td>Contact Name</td><td>{data.contact_name || '—'}</td></tr>
            <tr><td>Designation</td><td>{data.contact_designation || '—'}</td></tr>
            <tr><td>Mobile</td><td>{data.contact_mobile || '—'}</td></tr>
            <tr><td>Email</td><td>{data.contact_email || '—'}</td></tr>
            <tr><td>City / State</td><td>{data.city || '—'}</td></tr>
          </tbody>
        </table>
      </div>
      <div className="review-block">
        <div className="review-block-hd">Business & Partnership</div>
        <table className="review-tbl">
          <tbody>
            <tr><td>Top Destinations</td><td>{data.top_destinations || '—'}</td></tr>
            <tr><td>Monthly Bookings</td><td>{data.avg_monthly_bookings || '—'}</td></tr>
            <tr><td>Client Type</td><td>{data.client_types.join(', ') || '—'}</td></tr>
            <tr><td>Expected Nights/Month</td><td>{data.expected_monthly_room_nights || '—'}</td></tr>
            <tr><td>Room Category</td><td>{data.preferred_room_category || '—'}</td></tr>
            <tr><td>Commission Expected</td><td>{data.commission_requested || '—'}</td></tr>
            <tr><td>Payment Terms</td><td>{data.preferred_payment_terms || '—'}</td></tr>
          </tbody>
        </table>
      </div>
      <div className="review-block">
        <div className="review-block-hd">Banking, Documents & Declaration</div>
        <table className="review-tbl">
          <tbody>
            <tr><td>Bank Name</td><td>{data.bank_name || '—'}</td></tr>
            <tr><td>Account Name</td><td>{data.account_name || '—'}</td></tr>
            <tr><td>Account Number</td><td>{data.account_number || '—'}</td></tr>
            <tr><td>IFSC</td><td>{data.ifsc_code || '—'}</td></tr>
            <tr><td>GST Registration</td><td>{data.docs_gst ? 'Attached' : 'Not Attached'}</td></tr>
            <tr><td>PAN Card</td><td>{data.docs_pan ? 'Attached' : 'Not Attached'}</td></tr>
            <tr><td>Company Registration</td><td>{data.docs_company ? 'Attached' : 'Not Attached'}</td></tr>
            <tr><td>Cancelled Cheque</td><td>{data.docs_cheque ? 'Attached' : 'Not Attached'}</td></tr>
            <tr><td>Terms Agreed</td><td>{data.agreed ? '✓ Yes' : '✗ Not yet'}</td></tr>
            <tr><td>Authorized Signatory</td><td>{data.signatory_name || '—'}</td></tr>
            <tr><td>Name</td><td>{data.signatory_designation || '—'}</td></tr>
            <tr><td>Date</td><td>{data.signatory_date || '—'}</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function StepSuccess({ data, vendorId, config }) {
  return (
    <div className="step-panel active">
      <div className="success-wrap">
        <div className="success-ring"><svg viewBox="0 0 28 28"><polyline points="5,14 11,20 23,8" /></svg></div>
        <div className="success-title">Registration Submitted</div>
        <p className="success-sub">Thank you, {data.agency_name || 'your agency'}. Your registration with {config.RESORT_NAME} has been received and will be reviewed within 2–3 business days.</p>
        <div className="ref-pill">Reference ID &nbsp;·&nbsp; <strong>{vendorId}</strong></div>
        <div className="success-contact">
          For queries: <a href={`mailto:${config.CONTACT_EMAIL}`}>{config.CONTACT_EMAIL}</a> &nbsp;·&nbsp; <a href={`tel:${config.PHONE}`}>{config.PHONE}</a>
        </div>
      </div>
    </div>
  );
}
