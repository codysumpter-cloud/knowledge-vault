const { Plugin, ItemView, PluginSettingTab, Setting, Notice, TFile } = require('obsidian');
const VIEW_TYPE = 'bmo-command-center-view';
const SECRET_SERVICE = 'obsidian-bmo';
const SECRET_SLOTS = [
  ['openai-api-key', 'OpenAI API key'],
  ['anthropic-api-key', 'Anthropic API key'],
  ['openrouter-api-key', 'OpenRouter API key'],
  ['github-token', 'GitHub token / gh fallback'],
  ['appstore-connect-api-key', 'App Store Connect API key reference']
];
function ymd(d = new Date()) { return d.toISOString().slice(0, 10); }
async function ensureFolder(app, p) { if (!(await app.vault.adapter.exists(p))) await app.vault.createFolder(p); }
async function appendFile(app, p, text) { const f = app.vault.getAbstractFileByPath(p); if (f instanceof TFile) await app.vault.append(f, text); else await app.vault.create(p, text.replace(/^\n+/, '')); }
function runSecurity(args) {
  return new Promise((resolve, reject) => {
    let cp;
    try { cp = require('child_process').spawn('/usr/bin/security', args, { stdio: ['ignore', 'pipe', 'pipe'] }); }
    catch (e) { reject(e); return; }
    let out = '', err = '';
    cp.stdout.on('data', d => out += d.toString());
    cp.stderr.on('data', d => err += d.toString());
    cp.on('close', code => code === 0 ? resolve(out.trim()) : reject(new Error(err.trim() || `security exited ${code}`)));
  });
}
class View extends ItemView {
  constructor(leaf, plugin) { super(leaf); this.plugin = plugin; }
  getViewType() { return VIEW_TYPE; }
  getDisplayText() { return 'BMO Command Center'; }
  getIcon() { return 'bot'; }
  async onOpen() { this.render(); }
  render() {
    const c = this.containerEl.children[1]; c.empty(); c.addClass('bmo-command-center');
    const date = ymd();
    c.createEl('h1', { text: 'BMO Operational Command Center' });
    const hero = c.createDiv('bmo-hero');
    hero.createEl('div', { text: `Today: ${date}` });
    hero.createEl('div', { text: 'Capture → focus → execute → receipts → metrics intelligence.' });
    const a = hero.createDiv('bmo-actions');
    a.createEl('button', { text: 'Start / Today' }).onclick = () => this.plugin.startToday();
    a.createEl('button', { text: 'Close Day' }).onclick = () => this.plugin.closeDay();
    a.createEl('button', { text: 'Open Daily' }).onclick = () => this.plugin.openPath(`01-Dashboard/Daily/${date}.md`);
    a.createEl('button', { text: 'Open Activity' }).onclick = () => this.plugin.openPath(`01-Dashboard/Activity Log/${date}.md`);
    const grid = c.createDiv('bmo-grid');
    const focus = grid.createDiv('bmo-card');
    focus.createEl('h3', { text: 'Current Focus' });
    focus.createEl('p', { cls: 'bmo-focus', text: '1. TestFlight receipts: iOS Build 53 visible + macOS Build 6 blocker cleared' });
    focus.createEl('p', { text: 'Completion gate stays strict: visible to Cody or exact blocker captured.' });
    const cap = grid.createDiv('bmo-card');
    cap.createEl('h3', { text: 'Quick Capture → Inbox' });
    const ta = cap.createEl('textarea', { cls: 'bmo-textarea', placeholder: 'Idea, task, bug, receipt...' });
    cap.createEl('button', { text: 'Capture' }).onclick = async () => { await this.plugin.quickCapture(ta.value); ta.value = ''; };
    const metrics = grid.createDiv('bmo-card');
    metrics.createEl('h3', { text: 'Daily Metrics' });
    ['release receipts', 'profit actions', 'vault updates', 'agent runs', 'health/focus'].forEach(x => metrics.createEl('div', { text: '□ ' + x }));
    const links = grid.createDiv('bmo-card');
    links.createEl('h3', { text: 'Jump Links' });
    [['Live Dashboard', '00 - Command Center/BMO Operational Dashboard.md'], ['Mobile Command Center', '01-Dashboard/Mobile Command Center.md'], ['Inbox', '00-Inbox/Inbox.md'], ['Credential Index', '00-Private/Credentials/SECRET_INDEX.md'], ['iOS Receipt', '20 - Operations/Build 53 TestFlight Failure Receipt.md'], ['macOS Blocker', '20 - Operations/macOS Build 6 TestFlight Blocker.md']].forEach(([label, path]) => {
      const b = links.createEl('button', { text: label }); b.onclick = () => this.plugin.openPath(path);
    });
  }
}
class SecretSettingsTab extends PluginSettingTab {
  constructor(app, plugin) { super(app, plugin); this.plugin = plugin; }
  display() {
    const { containerEl } = this; containerEl.empty();
    containerEl.createEl('h2', { text: 'BMO Secrets' });
    containerEl.createEl('p', { text: 'Secrets entered here are written to macOS Keychain service obsidian-bmo. Values are not saved in Obsidian notes, plugin data.json, or workspace files.' });
    containerEl.createEl('p', { text: 'Leave a field blank unless you are rotating/adding that key. Use “Check” to verify a secret exists without revealing it.' });
    SECRET_SLOTS.forEach(([account, label]) => {
      let value = '';
      new Setting(containerEl)
        .setName(label)
        .setDesc(`Keychain account: ${SECRET_SERVICE}/${account}`)
        .addText(t => t.setPlaceholder('paste key only when saving').then(t => { t.inputEl.type = 'password'; t.onChange(v => value = v); }))
        .addButton(b => b.setButtonText('Save to Keychain').setCta().onClick(async () => {
          if (!value.trim()) { new Notice('No value entered; not saving.'); return; }
          try { await runSecurity(['add-generic-password', '-a', account, '-s', SECRET_SERVICE, '-w', value, '-U']); value = ''; new Notice(`Saved ${account} to macOS Keychain`); }
          catch (e) { new Notice(`Keychain save failed: ${e.message}`); }
        }))
        .addButton(b => b.setButtonText('Check').onClick(async () => {
          try { await runSecurity(['find-generic-password', '-a', account, '-s', SECRET_SERVICE]); new Notice(`${account}: present in Keychain`); }
          catch (_) { new Notice(`${account}: not found`); }
        }))
        .addButton(b => b.setButtonText('Delete').onClick(async () => {
          try { await runSecurity(['delete-generic-password', '-a', account, '-s', SECRET_SERVICE]); new Notice(`${account}: deleted from Keychain`); }
          catch (_) { new Notice(`${account}: not found / delete skipped`); }
        }));
    });
  }
}
module.exports = class BMO extends Plugin {
  async onload() {
    this.registerView(VIEW_TYPE, leaf => new View(leaf, this));
    this.addSettingTab(new SecretSettingsTab(this.app, this));
    this.addRibbonIcon('bot', 'Open BMO Command Center', () => this.activateView());
    this.addCommand({ id: 'open', name: 'BMO: Open Command Center', callback: () => this.activateView() });
    this.addCommand({ id: 'today', name: 'BMO: /today - start daily operating loop', callback: () => this.startToday() });
    this.addCommand({ id: 'close-day', name: 'BMO: /close-day - close daily metrics and log', callback: () => this.closeDay() });
    this.addCommand({ id: 'quick-capture', name: 'BMO: Quick capture to inbox', callback: () => this.quickCapture('Manual quick capture placeholder — edit this line.') });
    this.addCommand({ id: 'open-secret-index', name: 'BMO: Open secret index', callback: () => this.openPath('00-Private/Credentials/SECRET_INDEX.md') });
  }
  async activateView() { const leaf = this.app.workspace.getLeaf(true); await leaf.setViewState({ type: VIEW_TYPE, active: true }); this.app.workspace.revealLeaf(leaf); }
  async openPath(p) { const f = this.app.vault.getAbstractFileByPath(p); if (f instanceof TFile) await this.app.workspace.getLeaf(true).openFile(f); else new Notice('Missing note: ' + p); }
  async startToday() {
    const date = ymd(); await ensureFolder(this.app, '01-Dashboard/Daily'); await ensureFolder(this.app, '01-Dashboard/Activity Log');
    if (!(await this.app.vault.adapter.exists(`01-Dashboard/Daily/${date}.md`))) await this.app.vault.create(`01-Dashboard/Daily/${date}.md`, `---\ndate: ${date}\nstatus: active\nrelease_receipts: 0\nprofit_actions: 0\nvault_updates: 0\nagent_runs: 0\nfocus_score:\n---\n# Daily Command Note — ${date}\n\n## Top 3 Priorities\n- [ ] iOS Build visible in TestFlight or exact blocker captured\n- [ ] macOS Build visible in TestFlight or exact blocker captured\n- [ ] Obsidian OS operated today\n\n## Current Focus\n\n## Tasks\n\n## Activity Log\n![[${date}]]\n\n## Close Day Notes\n`);
    await appendFile(this.app, `01-Dashboard/Activity Log/${date}.md`, `\n- ${new Date().toLocaleTimeString()} — /today started.\n`);
    await this.openPath(`01-Dashboard/Daily/${date}.md`); new Notice('BMO /today initialized');
  }
  async closeDay() { const date = ymd(); await appendFile(this.app, `01-Dashboard/Activity Log/${date}.md`, `\n- ${new Date().toLocaleTimeString()} — /close-day checkpoint. Metrics ready for review.\n`); await this.openPath(`01-Dashboard/Activity Log/${date}.md`); new Notice('BMO day close checkpoint logged'); }
  async quickCapture(text) { const date = ymd(); const body = (text || '').trim(); if (!body) { new Notice('Nothing to capture'); return; } await ensureFolder(this.app, '00-Inbox'); await appendFile(this.app, '00-Inbox/Inbox.md', `\n- ${date} ${new Date().toLocaleTimeString()} — ${body}\n`); new Notice('Captured to inbox'); }
};
