import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { predictionService } from '../services/predictionService';
import { patientService } from '../services/patientService';
import { Patient } from '../types';
import { Upload, AlertCircle, ArrowRight, Activity, Database, FileText, Brain, Radio } from 'lucide-react';

export const UploadScanPage: React.FC = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('');
  const [modality, setModality] = useState<string>('CHEST_XRAY');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    patientService.getAll().then((data) => {
      setPatients(data);
      if (data.length > 0) setSelectedPatientId(data[0].id);
    }).catch(console.error);
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setError(null);
    }
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile || !selectedPatientId) {
      setError('Please select a patient profile and upload a valid medical image scan.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const imageRecord = await predictionService.uploadImage(selectedFile, selectedPatientId, modality);
      const prediction = await predictionService.analyzeImage(imageRecord.id, 'RESNET50');

      navigate(`/prediction/${prediction.id}`, { state: { prediction, image: imageRecord } });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload and analyze image scan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div>
        <div className="flex items-center space-x-2">
          <Database className="w-5 h-5 text-amber-400" />
          <h1 className="text-2xl font-black text-white uppercase tracking-tight">Multi-Modality Scan Viewport</h1>
        </div>
        <p className="text-xs text-slate-400 font-medium">
          Official Dataset Modalities: Chest X-Ray (4 Classes), Brain MRI (4 Classes), Lung CT (3 Classes)
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      <div className="gold-panel p-6 rounded-3xl space-y-6">
        {/* Dataset Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div className="space-y-1">
            <label className="text-xs font-black text-amber-200 uppercase tracking-wider">Patient History & Metadata</label>
            <select
              value={selectedPatientId}
              onChange={(e) => setSelectedPatientId(e.target.value)}
              className="w-full py-3 px-3.5 rounded-xl bg-[#0a0c16] border border-amber-500/30 text-xs text-white focus:outline-none focus:border-amber-400 font-medium"
            >
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.patient_code} - Age {p.age} ({p.gender})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1">
            <label className="text-xs font-black text-amber-200 uppercase tracking-wider">Scan Modality Target</label>
            <select
              value={modality}
              onChange={(e) => setModality(e.target.value)}
              className="w-full py-3 px-3.5 rounded-xl bg-[#0a0c16] border border-amber-500/30 text-xs text-white focus:outline-none focus:border-amber-400 font-medium"
            >
              <option value="CHEST_XRAY">Dataset 1: Chest X-Ray (Normal, COVID-19, Pneumonia, Tuberculosis)</option>
              <option value="BRAIN_MRI">Dataset 2: Brain MRI (Glioma, Meningioma, Pituitary, No Tumor)</option>
              <option value="LUNG_CT">Dataset 3: Lung CT Scan (Benign, Malignant, Normal)</option>
            </select>
          </div>
        </div>

        {/* Modality Specific Pipeline Information Card */}
        <div className="p-4 rounded-2xl bg-[#0a0c16] border border-amber-500/20 text-xs space-y-1">
          <div className="flex items-center space-x-2 font-black text-amber-400 uppercase tracking-wider">
            <Radio className="w-4 h-4 text-amber-400" />
            <span>Preprocessing Pipeline & Model Router</span>
          </div>
          <p className="text-slate-300">
            {modality === 'BRAIN_MRI'
              ? 'Brain MRI Pipeline: Skull Stripping (Otsu contour mask) ➔ Bias Field Correction ➔ EfficientNet-B0 Classifier.'
              : modality === 'LUNG_CT'
              ? 'Lung CT Pipeline: Hounsfield Windowing ➔ Contrast Enhancement ➔ ResNet18 Transfer Learning Classifier.'
              : 'Chest X-Ray Pipeline: CLAHE Contrast Enhancement ➔ Denoising ➔ ResNet50 Classifier + Grad-CAM Visual Heatmap.'}
          </p>
        </div>

        {/* Drag and Drop Zone */}
        <div className="border-2 border-dashed border-amber-500/30 hover:border-amber-400 rounded-2xl p-8 text-center bg-[#0a0c16]/60 transition-colors relative">
          <input
            type="file"
            accept=".png,.jpg,.jpeg,.dcm"
            onChange={handleFileSelect}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />

          {previewUrl ? (
            <div className="space-y-3 flex flex-col items-center">
              <img src={previewUrl} alt="Scan preview" className="max-h-64 rounded-xl border border-amber-500/30 shadow-xl object-contain" />
              <p className="text-xs text-amber-400 font-mono font-bold">{selectedFile?.name}</p>
            </div>
          ) : (
            <div className="space-y-3 flex flex-col items-center">
              <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shadow-md">
                <Upload className="w-6 h-6 stroke-[2.5]" />
              </div>
              <div>
                <p className="text-sm font-black text-white uppercase tracking-wider">Drag & drop medical image here</p>
                <p className="text-xs text-slate-400 font-medium mt-1">Supports DICOM, PNG, and JPEG files up to 50MB</p>
              </div>
            </div>
          )}
        </div>

        <button
          onClick={handleUploadAndAnalyze}
          disabled={loading || !selectedFile}
          className="w-full py-4 rounded-2xl gold-button text-slate-950 font-black text-xs transition-all shadow-xl flex items-center justify-center space-x-2 disabled:opacity-50 uppercase tracking-wider"
        >
          <span>{loading ? 'Executing Modality Pipeline & Grad-CAM...' : 'Analyze Image Scan'}</span>
          <ArrowRight className="w-4 h-4 stroke-[2.5]" />
        </button>
      </div>
    </div>
  );
};

export default UploadScanPage;
