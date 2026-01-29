<template>
  <div class="app">
    <header class="header">
      <div class="header-row">
        <div class="header-left">
          <div class="header-icon"></div>
          <div class="header-text">
            <h1>Reports Dashboard</h1>
            <span class="header-subtitle"
              >Manage and review your generated reports</span
            >
          </div>
        </div>

        <div class="header-right">
          <span class="header-count">{{ reports.length }}</span>
          <span class="header-count-label"> reports</span>
        </div>
      </div>
    </header>

    <!-- Loading/Error states -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading reports...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <div class="error-icon">⚠️</div>
      <p>{{ error }}</p>
    </div>

    <div v-else-if="reports.length === 0" class="empty-state">
      <div class="empty-icon">📁</div>
      <h3>No reports found</h3>
      <p>Add files to <code>backend/reports/</code></p>
    </div>

    <!-- Reports grid -->
    <div v-else class="reports-grid">
      <div
        v-for="(report, index) in reports"
        :key="report.name"
        class="report-card"
      >
        <!-- Add position number -->
        <div class="report-position">{{ index + 1 }}</div>

        <div class="card-header">
          <div class="file-icon">{{ getFileIcon(report.name) }}</div>
          <div class="file-meta">
            <h3 class="file-name">{{ report.name }}</h3>
            <div class="file-info">
              <span class="size">{{ formatSize(report.size) }}</span>
              <span class="date">{{ formatDate(report.modified) }}</span>
            </div>
          </div>
        </div>

        <div class="card-actions">
          <a
            :href="`/api/reports/${report.name}`"
            target="_blank"
            class="btn-primary"
          >
            <svg class="icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z" />
            </svg>
            Download
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";

interface Report {
  name: string;
  size: number;
  modified: string;
}

const reports = ref<Report[]>([]);
const loading = ref(true);
const error = ref("");

onMounted(async () => {
  try {
    const response = await axios.get("/api/reports");
    reports.value = response.data;
  } catch (err: any) {
    error.value = err.message || "Failed to load reports";
  } finally {
    loading.value = false;
    await initDialOverlay();
  }
});

const initDialOverlay = async () => {
  try {
    const { ChatOverlay } = await import("@epam/ai-dial-overlay");

    const container = document.createElement("div");
    container.id = "dial-overlay-container";
    container.style.cssText = `
      position: fixed !important;
      right: 20px !important;
      bottom: 20px !important;
      z-index: 9999 !important;
      pointer-events: none;
      width: 360px;
      height: 480px;
    `;
    document.body.appendChild(container);

    const overlay = new ChatOverlay(container, {
      hostDomain: window.location.origin,
      domain: "http://localhost:3000",
      theme: "light",
      modelId: "talk-to-your-document-agent",
      requestTimeout: 20000,
    });

    await overlay.ready();

    const iframe = container.querySelector("iframe") as HTMLIFrameElement;
    if (iframe) {
      iframe.style.pointerEvents = "auto";
      iframe.style.borderRadius = "16px";
      iframe.style.boxShadow = "0 20px 40px rgba(0,0,0,0.15)";
    }
  } catch (err) {
    console.error("Overlay init failed:", err);
  }
};

const getFileIcon = (filename: string) => {
  const ext = filename.split(".").pop()?.toLowerCase();
  const icons: Record<string, string> = {
    pdf: "📄",
    xlsx: "📊",
    xls: "📊",
    docx: "📝",
    doc: "📝",
    txt: "📄",
    png: "🖼️",
    jpg: "🖼️",
    jpeg: "🖼️",
    gif: "🖼️",
  };
  return icons[ext || ""] || "📎";
};

const formatSize = (bytes: number): string => {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
};

const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString("uk-UA");
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.app {
  min-height: 100vh;
  padding: 2rem 2rem 2rem 2rem;
  margin: 0;
  width: 100vw;
  max-width: 1000px;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.header {
  width: 100%;
  padding: 1.5rem 2.5rem;
  margin: 0 0 1.5rem 0;
  background: transparent;
  box-shadow: none;
  border: none;
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
}

.header-text h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 800;
  color: #f9fafb;
}

.header-subtitle {
  display: block;
  margin-top: 0.2rem;
  font-size: 0.85rem;
  color: #cbd5f5;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  line-height: 1.1;
}

.header-count {
  font-size: 1.6rem;
  font-weight: 800;
  color: #a5b4fc;
}

.header-count-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #9ca3af;
}

.loading-container,
.error-container,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  margin: 2rem 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.error-icon,
.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state code {
  background: #64748b;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-size: 0.9rem;
}

.report-position {
  position: absolute;
  left: -2.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.75rem;
  height: 1.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 700;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.reports-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 0 4rem 4rem 6.5rem;
  max-width: none;
}

.report-card:hover .report-position {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: rgba(102, 126, 234, 0.4);
}
.report-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1rem 1.25rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 65px;
  display: flex;
  align-items: center;
  position: relative;
  overflow: visible;
}

.report-card:hover .report-position {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: rgba(102, 126, 234, 0.4);
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
  border-color: rgba(102, 126, 234, 0.4);
}

.card-header {
  display: flex;
  gap: 0.75rem;
  flex: 1;
  align-items: flex-start;
  min-width: 0;
}

.file-icon {
  font-size: 1.75rem;
  flex-shrink: 0;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.1));
  margin-top: 0.15rem;
}

.file-meta {
  flex: 1;
  min-width: 0;
}

.file-meta h3 {
  margin: 0 0 0.25rem 0;
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-info {
  display: flex;
  gap: 1rem;
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

.file-name {
  text-align: left !important;
  margin-left: 0 !important;
  padding-left: 0 !important;
}

.card-actions {
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.report-card:hover .card-actions {
  opacity: 1;
  visibility: visible;
  transform: translateY(-50%) translateX(4px);
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white !important;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.8rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.25s ease;
  white-space: nowrap;
}

.btn-primary:hover {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

.icon {
  width: 14px;
  height: 14px;
}

#dial-overlay-container iframe {
  pointer-events: auto !important;
  border-radius: 16px !important;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

@media (max-width: 768px) {
  .app {
    padding: 1.5rem 1rem;
  }

  .reports-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }

  .report-card {
    min-height: 60px;
    padding: 0.875rem 1rem;
  }

  .header {
    padding: 1.5rem 1.5rem;
  }

  .header-content {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .title {
    font-size: 2rem;
  }
}
</style>
