import axios from 'axios';

const API_BASE = '/api';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Attach token if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('smartcare_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  forgotPassword: (emailOrId) => api.post('/auth/forgot-password', { email_or_id: emailOrId }),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me')
};

export const patientAPI = {
  getProfile: () => api.get('/patients/profile'),
  updateProfile: (profileData) => api.put('/patients/profile', profileData)
};

export const healthDataAPI = {
  submitRecord: (data) => api.post('/health-data/submit', data),
  getRecords: () => api.get('/health-data/records')
};

export const datasetAPI = {
  list: () => api.get('/datasets/list'),
  getProfile: (name) => api.get(`/datasets/${name}/profile`),
  getMissingness: (name) => api.get(`/datasets/${name}/missingness`),
  getVif: (name) => api.get(`/datasets/${name}/vif`),
  getFeatureMapping: () => api.get('/datasets/feature-mapping')
};

export const pipelineAPI = {
  run: (config) => api.post('/pipelines/run', config),
  getExperiments: (name) => api.get('/pipelines/experiments', { params: { dataset_name: name } })
};

export const predictionAPI = {
  predictMultiRisk: (data) => api.post('/predictions', data),
  getEvaluation: (disease) => api.get(`/models/evaluations/${disease}`)
};

export const recommendationAPI = {
  generatePlan: (data) => api.post('/recommendations/generate', data),
  getByPatient: (patientId) => api.get(`/recommendations/patient/${patientId}`),
  getByAssessment: (assessmentId) => api.get(`/recommendations/assessment/${assessmentId}`)
};

export const riskMonitoringAPI = {
  getRiskHistory: (patientId) => api.get(`/risk-history/${patientId}`),
  getRiskTrends: (patientId) => api.get(`/risk-history/${patientId}/trends`),
  getAssessmentDetails: (assessmentId) => api.get(`/assessments/${assessmentId}`),
  getPatientAlerts: (patientId) => api.get(`/alerts/${patientId}`),
  updateAlertStatus: (alertId, statusData) => api.put(`/alerts/${alertId}`, statusData)
};

export const clinicianAPI = {
  getDashboard: () => api.get('/clinician/dashboard'),
  getPatientList: () => api.get('/clinician/patients'),
  getPatientDetail: (patientId) => api.get(`/clinician/patients/${patientId}`),
  submitFeedback: (feedbackData) => api.post('/clinician/feedback', feedbackData)
};

export const chatAPI = {
  sendMessage: (message, session_id = 'default') => api.post('/chat', { message, session_id }),
  getHistory: (session_id = 'default') => api.get('/chat/history', { params: { session_id } })
};

export const dashboardAPI = {
  getOverview: () => api.get('/dashboard/overview')
};

export const adminAPI = {
  listPatients: () => api.get('/admin/patients'),
  listDoctors: (statusFilter) => api.get('/admin/doctors', { params: statusFilter ? { status_filter: statusFilter } : {} }),
  verifyDoctor: (doctorId, status) => api.put(`/admin/doctors/${doctorId}/verify`, { verification_status: status }),
  updateUserStatus: (userId, status) => api.put(`/admin/users/${userId}/status`, { status }),
  resetUserPassword: (userId) => api.post(`/admin/users/${userId}/reset-password`),
  createStaffUser: (userData) => api.post('/admin/users', userData),
  listAdmins: () => api.get('/admin/admins'),
  createAdmin: (adminData) => api.post('/admin/admins', adminData),
  getAuditLogs: (limit = 100) => api.get('/admin/audit-logs', { params: { limit } }),
  getSystemAnalytics: () => api.get('/admin/analytics'),
  getSystemSettings: () => api.get('/admin/settings'),
  updateSystemSettings: (data) => api.put('/admin/settings', data),
  getDoctorAssignments: () => api.get('/admin/doctor-assignments'),
  assignDoctorPatient: (data) => api.post('/admin/doctor-assignments', data),
  removeDoctorPatientAssignment: (doctorId, patientId) => api.delete(`/admin/doctor-assignments/${doctorId}/${patientId}`),
  reindexDatabase: () => api.post('/admin/operations/reindex'),
  clearCache: () => api.post('/admin/operations/clear-cache'),
  generateBackup: () => api.post('/admin/operations/backup'),
  broadcastNotice: (data) => api.post('/admin/broadcast', data),
  requestResetOTP: () => api.post('/admin/system/request-reset-otp'),
  systemFactoryReset: (data) => api.post('/admin/system/factory-reset', data)
};

export const notificationAPI = {
  getUserNotifications: () => api.get('/notifications'),
  markRead: (id) => api.put(`/notifications/${id}/read`)
};

export const reportAPI = {
  getMyReports: () => api.get('/reports/my-reports'),
  generateReport: (predictionId) => api.post(`/reports/generate/${predictionId}`),
  generateReportForPatient: (patientId) => api.post(`/reports/generate/patient/${patientId}`),
  getPatientReports: (patientId) => api.get(`/reports/patient/${patientId}`),
  getReportDetails: (reportId) => api.get(`/reports/${reportId}/view`),
  updateReportVisibility: (reportId, patientVisible) => api.put(`/reports/${reportId}/visibility`, { patient_visible: patientVisible }),
  downloadReportBlob: (reportId, inline = true) => api.get(`/reports/${reportId}/download`, {
    params: { inline },
    responseType: 'blob'
  }),
  getDownloadUrl: (reportId, inline = true) => {
    const token = localStorage.getItem('smartcare_token') || localStorage.getItem('token') || '';
    return `/api/reports/${reportId}/download?inline=${inline}${token ? `&token=${encodeURIComponent(token)}` : ''}`;
  },
  reviewReport: (reportId, reviewData) => api.put(`/reports/${reportId}/review`, reviewData)
};

export default api;

