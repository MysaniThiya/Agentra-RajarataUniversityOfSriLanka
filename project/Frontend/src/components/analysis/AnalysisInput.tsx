import { Mail, Link2, Upload, FileText, Loader2, ShieldAlert, Sparkles } from 'lucide-react';
import { useRef, useState } from 'react';
import { Button } from '@/components/ui/Button';

type Mode = 'email' | 'url';

interface AnalysisInputProps {
  mode: Mode;
  onAnalyze: (input: string) => void;
  loading: boolean;
}

export function AnalysisInput({ mode, onAnalyze, loading }: AnalysisInputProps) {
  const [emailText, setEmailText] = useState('');
  const [urlText, setUrlText] = useState('');
  const [fileName, setFileName] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) setFileName(f.name);
  };

  const canSubmit =
    !loading && (mode === 'email' ? emailText.trim().length > 0 : urlText.trim().length > 0);

  const handleSubmit = () => {
    onAnalyze(mode === 'email' ? emailText.trim() : urlText.trim());
  };

  if (mode === 'email') {
    return (
      <div className="space-y-4 animate-fade-in">
        <div>
          <label className="flex items-center gap-2 text-sm font-semibold text-navy-800 mb-2">
            <Mail className="h-4 w-4 text-iris-600" />
            Paste email content
          </label>
          <textarea
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
            placeholder="Paste the full email here — headers, sender, subject, and body for the most accurate analysis..."
            rows={8}
            className="input-field font-mono text-[13px] leading-relaxed resize-y"
          />
          <p className="mt-1.5 text-xs text-navy-400">
            {emailText.length.toLocaleString()} characters
          </p>
        </div>

        <div>
          <label className="flex items-center gap-2 text-sm font-semibold text-navy-800 mb-2">
            <Upload className="h-4 w-4 text-iris-600" />
            Or upload an email file <span className="text-navy-400 font-normal">(optional)</span>
          </label>
          <div
            onClick={() => fileRef.current?.click()}
            className="group cursor-pointer rounded-xl border-2 border-dashed border-navy-200 hover:border-iris-400 hover:bg-iris-50/40 transition px-4 py-6 text-center"
          >
            <input
              ref={fileRef}
              type="file"
              accept=".eml,.msg,.txt"
              className="hidden"
              onChange={handleFile}
            />
            {fileName ? (
              <div className="flex items-center justify-center gap-2 text-navy-700">
                <FileText className="h-5 w-5 text-iris-600" />
                <span className="font-medium">{fileName}</span>
              </div>
            ) : (
              <>
                <Upload className="mx-auto h-7 w-7 text-navy-300 group-hover:text-iris-500 transition" />
                <p className="mt-2 text-sm text-navy-500">
                  Click to upload <span className="font-medium text-navy-700">.eml</span>,{' '}
                  <span className="font-medium text-navy-700">.msg</span>, or{' '}
                  <span className="font-medium text-navy-700">.txt</span>
                </p>
              </>
            )}
          </div>
        </div>

        <Button size="lg" onClick={handleSubmit} disabled={!canSubmit} className="w-full sm:w-auto">
          {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Sparkles className="h-5 w-5" />}
          {loading ? 'Analyzing Email...' : 'Analyze Email'}
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-4 animate-fade-in">
      <div>
        <label className="flex items-center gap-2 text-sm font-semibold text-navy-800 mb-2">
          <Link2 className="h-4 w-4 text-iris-600" />
          Enter suspicious URL
        </label>
        <div className="relative">
          <input
            type="text"
            value={urlText}
            onChange={(e) => setUrlText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && canSubmit && handleSubmit()}
            placeholder="https://example-suspicious-site.com/login"
            className="input-field font-mono text-[13px] pr-10"
          />
          <Link2 className="absolute right-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-navy-300" />
        </div>
        <p className="mt-1.5 text-xs text-navy-400">
          Include the full address with protocol (http / https).
        </p>
      </div>

      <div className="rounded-xl bg-navy-50 border border-navy-100 p-3.5 flex gap-2.5">
        <ShieldAlert className="h-4.5 w-4.5 text-amber-500 shrink-0 mt-0.5" />
        <p className="text-xs text-navy-600 leading-relaxed">
          PhishGuard AI examines the URL's structure and reputation without visiting the page.
          Avoid entering credentials on any suspicious link.
        </p>
      </div>

      <Button size="lg" onClick={handleSubmit} disabled={!canSubmit} className="w-full sm:w-auto">
        {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Sparkles className="h-5 w-5" />}
        {loading ? 'Analyzing URL...' : 'Analyze URL'}
      </Button>
    </div>
  );
}
