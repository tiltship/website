{{/*
TILTSHIP COMMON VALUES
*/}}

{{- define "tiltship.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "tiltship.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "tiltship.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "tiltship.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "tiltship.labels" -}}
helm.sh/chart: {{ include "tiltship.chart" . }}
app.kubernetes.io/part-of: {{ include "tiltship.fullname" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
COATCHECK - TODO: automate this for more services
*/}}

{{- define "coatcheck.fullname" -}}
{{- printf "%s-%s" (include "tiltship.fullname" .) "coatcheck" | trunc 63 | trimSuffix "-" }}
{{- end}}

{{- define "coatcheck.selectorLabels" -}}
app.kubernetes.io/name: {{ include "tiltship.name" . }}-coatcheck
app.kubernetes.io/instance: {{ include "coatcheck.fullname" . }}
app.kubernetes.io/version: {{ .Values.coatcheck.image.tag | quote }}
helm.sh/release: {{ .Release.Name }}
release: {{ .Release.Name }}
{{- end }}
