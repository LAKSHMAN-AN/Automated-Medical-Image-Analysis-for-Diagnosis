import React, { useEffect, useState } from 'react';
import { patientService } from '../services/patientService';
import { Patient } from '../types';
import { Plus } from 'lucide-react';

export const PatientManagementPage: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [patientCode, setPatientCode] = useState('');
  const [age, setAge] = useState<number>(45);
  const [gender, setGender] = useState('MALE');
  const [medicalHistory, setMedicalHistory] = useState('');

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = () => {
    patientService.getAll()
      .then(setPatients)
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  const handleCreatePatient = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await patientService.create({
        patient_code: patientCode,
        age,
        gender,
        medical_history: medicalHistory,
      });
      setShowModal(false);
      fetchPatients();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Patient Record Registry</h1>
          <p className="text-xs text-slate-400">Anonymized clinical profiles and historical scan records</p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs transition-all flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>Register New Patient</span>
        </button>
      </div>

      <div className="glass-panel rounded-2xl border-slate-800 overflow-hidden">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-900/80 text-slate-400 font-mono text-[11px] uppercase border-b border-slate-800">
            <tr>
              <th className="p-4">Patient Code</th>
              <th className="p-4">Age</th>
              <th className="p-4">Gender</th>
              <th className="p-4">Medical History Summary</th>
              <th className="p-4">Registered Date</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-200">
            {loading ? (
              <tr>
                <td colSpan={5} className="p-8 text-center text-slate-500">Loading patient registry...</td>
              </tr>
            ) : patients.length === 0 ? (
              <tr>
                <td colSpan={5} className="p-8 text-center text-slate-500">No patient records registered yet.</td>
              </tr>
            ) : (
              patients.map((p) => (
                <tr key={p.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="p-4 font-mono font-bold text-cyan-400">{p.patient_code}</td>
                  <td className="p-4 font-mono">{p.age}</td>
                  <td className="p-4">{p.gender}</td>
                  <td className="p-4 text-slate-400 max-w-xs truncate">{p.medical_history || 'N/A'}</td>
                  <td className="p-4 font-mono text-slate-500">{new Date(p.created_at).toLocaleDateString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-md glass-panel p-6 rounded-2xl border-slate-800 space-y-4">
            <h3 className="text-lg font-bold text-white">Register Patient Profile</h3>

            <form onSubmit={handleCreatePatient} className="space-y-3">
              <div>
                <label className="text-xs text-slate-300">Patient Code</label>
                <input
                  type="text"
                  required
                  placeholder="PAT-2026-002"
                  value={patientCode}
                  onChange={(e) => setPatientCode(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-slate-300">Age</label>
                  <input
                    type="number"
                    required
                    value={age}
                    onChange={(e) => setAge(Number(e.target.value))}
                    className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-300">Gender</label>
                  <select
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  >
                    <option value="MALE">Male</option>
                    <option value="FEMALE">Female</option>
                    <option value="OTHER">Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-xs text-slate-300">Medical History</label>
                <textarea
                  rows={3}
                  placeholder="Acute symptoms, comorbidities, prior respiratory illness..."
                  value={medicalHistory}
                  onChange={(e) => setMedicalHistory(e.target.value)}
                  className="w-full p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-900 text-slate-400 text-xs hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs hover:bg-cyan-400"
                >
                  Save Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PatientManagementPage;
