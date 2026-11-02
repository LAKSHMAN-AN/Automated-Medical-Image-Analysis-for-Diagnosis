import { api } from './api';
import { MedicalImage, Prediction } from '../types';

export const predictionService = {
  async uploadImage(file: File, patientId: string, modality: string = 'CHEST_XRAY'): Promise<MedicalImage> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('patient_id', patientId);
    formData.append('modality', modality);

    const res = await api.post<MedicalImage>('/images/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  async analyzeImage(imageId: string, modelType: string = 'RESNET50'): Promise<Prediction> {
    const res = await api.post<Prediction>('/predictions/analyze', {
      image_id: imageId,
      model_type: modelType,
      include_gradcam: true,
    });
    return res.data;
  }
};
