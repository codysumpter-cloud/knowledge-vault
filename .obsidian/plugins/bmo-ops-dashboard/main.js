
const { Plugin, Notice, Modal, Setting, moment } = require('obsidian');

const DAILY_DIR = '01-Dashboard/Daily';
const INBOX_DIR = '00-Inbox/Captures';
const ACTIVITY_DIR = '01-Dashboard/Activity Log';
const DASHBOARD = '01-Dashboard/Live Command Center.md';

module.exports = class BMOOpsDashboard extends Plugin {
  async onload() {
    await this.ensureFolders();
    this.addCommand({ id: 'bmo-open-dashboard', name: 'Open Live Command Center', callback: () => this.openDashboard() });
    this.addCommand({ id: 'bmo-today', name: '/today — Start day and build focus note', callback: () => this.startDay() });
    this.addCommand({ id: 'bmo-close-day', name: '/close-day — Close day with metrics/reflection', callback: () => this.closeDay() });
    this.addCommand({ id: 'bmo-quick-capture', name: 'Quick capture to inbox', callback: () => this.quickCapture() });
    this.addCommand({ id: 'bmo-log-activity', name: 'Log activity', callback: () => this.logActivity() });
    this.addRibbonIcon('layout-dashboard', 'BMO Command Center', () => this.openDashboard());
    this.registerEvent(this.app.workspace.on('file-open', (file) => { if (file) this.appendActivity(`Opened [[${file.basename}]]`); }));
    new Notice('BMO Ops Dashboard loaded');
  }

  async ensureFolders() {
    for (const f of [DAILY_DIR, INBOX_DIR, ACTIVITY_DIR, '01-Dashboard/Metrics']) {
      if (!(await this.app.vault.adapter.exists(f))) await this.app.vault.createFolder(f);
    }
  }

  todayName() { return moment().format('YYYY-MM-DD'); }
  todayPath() { return `${DAILY_DIR}/${this.todayName()}.md`; }
  activityPath() { return `${ACTIVITY_DIR}/${this.todayName()}.md`; }

  async openFile(path) {
    const file = this.app.vault.getAbstractFileByPath(path);
    if (file) await this.app.workspace.getLeaf(false).openFile(file);
  }
  async openDashboard() { await this.ensureDashboard(); await this.openFile(DASHBOARD); }

  async ensureDashboard() {
    if (await this.app.vault.adapter.exists(DASHBOARD)) return;
    await this.app.vault.create(DASHBOARD, `# Live Command Center\n\n> One screen for focus, quick capture, metrics, and execution.\n\n## Start / Close\n- Run command: **BMO Ops Dashboard: /today — Start day and build focus note**\n- Run command: **BMO Ops Dashboard: /close-day — Close day with metrics/reflection**\n\n## Current Focus\n![[${this.todayPath()}]]\n\n## Quick Links\n- [[Home]]\n- [[01-Dashboard/Operator Dashboard|Operator Dashboard]]\n- [[01-Dashboard/Metrics/Metrics Index|Metrics Index]]\n- [[01-Dashboard/Activity Log/${this.todayName()}|Today Activity Log]]\n- [[00-Inbox/Captures|Captures Folder]]\n- [[04-Runbooks/Agent Workflows/BMO Daily Ops|BMO Daily Ops Runbook]]\n`);
  }

  async startDay() {
    await this.ensureFolders();
    const path = this.todayPath();
    if (!(await this.app.vault.adapter.exists(path))) {
      const yesterday = moment().subtract(1, 'day').format('YYYY-MM-DD');
      const content = `---\ndate: ${this.todayName()}\nstatus: active\nenergy: \nfocus_score: \nrevenue: \ntrading_pnl: \nyoutube_progress: \nfamily_time: \nhealth: \neffort: \n---\n# ${this.todayName()} Daily Command Note\n\n## Current Focus\n- [ ] Define ONE primary target\n\n## Top 3 Priorities\n- [ ] Priority 1\n- [ ] Priority 2\n- [ ] Priority 3\n\n## Carryover Review\n- Review yesterday: [[${yesterday}]]\n\n## Metrics\n- Energy: \n- Focus score: \n- Revenue: \n- Trading P/L: \n- YouTube progress: \n- Family time: \n- Health: \n- Effort /10: \n\n## Schedule / Calendar\n- \n\n## Activity Log\n![[${ACTIVITY_DIR}/${this.todayName()}]]\n\n## Notes\n- \n`;
      await this.app.vault.create(path, content);
      await this.appendActivity('Started day with /today');
      new Notice('Created today note');
    } else {
      await this.appendActivity('Opened existing today note with /today');
      new Notice('Today note already exists');
    }
    await this.openFile(path);
  }

  async closeDay() {
    await this.startDay();
    const text = await this.prompt('Close Day', 'Dictate/write reflection, wins, metrics, and carryovers:');
    if (!text) return;
    await this.appendToFile(this.todayPath(), `\n## Close Day Reflection\n${text}\n\n## Carryovers\n- [ ] \n`);
    await this.appendActivity('Closed day with /close-day');
    new Notice('Day closed');
  }

  async quickCapture() {
    const text = await this.prompt('Quick Capture', 'Capture idea/task/link:');
    if (!text) return;
    const stamp = moment().format('YYYY-MM-DD-HHmmss');
    const path = `${INBOX_DIR}/${stamp}.md`;
    await this.app.vault.create(path, `---\ncreated: ${moment().format()}\nstatus: inbox\n---\n# Capture ${stamp}\n\n${text}\n`);
    await this.appendActivity(`Quick captured [[${path.replace(/\.md$/, '')}]]`);
    new Notice('Captured to inbox');
  }

  async logActivity() {
    const text = await this.prompt('Log Activity', 'What did you just do?');
    if (!text) return;
    await this.appendActivity(text);
    new Notice('Activity logged');
  }

  async appendActivity(text) {
    const path = this.activityPath();
    const line = `- ${moment().format('HH:mm')} — ${text}\n`;
    await this.appendToFile(path, line, `# Activity Log ${this.todayName()}\n\n`);
  }

  async appendToFile(path, text, initial='') {
    if (!(await this.app.vault.adapter.exists(path))) await this.app.vault.create(path, initial);
    const file = this.app.vault.getAbstractFileByPath(path);
    if (file) await this.app.vault.append(file, text);
  }

  prompt(title, placeholder) {
    return new Promise((resolve) => {
      const modal = new TextInputModal(this.app, title, placeholder, resolve);
      modal.open();
    });
  }
}

class TextInputModal extends Modal {
  constructor(app, title, placeholder, onSubmit) { super(app); this.title = title; this.placeholder = placeholder; this.onSubmit = onSubmit; }
  onOpen() {
    const { contentEl } = this;
    contentEl.createEl('h2', { text: this.title });
    let value = '';
    new Setting(contentEl).addTextArea((text) => {
      text.setPlaceholder(this.placeholder);
      text.inputEl.rows = 8;
      text.inputEl.cols = 50;
      text.onChange((v) => value = v);
      setTimeout(() => text.inputEl.focus(), 50);
    });
    new Setting(contentEl)
      .addButton((btn) => btn.setButtonText('Cancel').onClick(() => { this.close(); this.onSubmit(null); }))
      .addButton((btn) => btn.setCta().setButtonText('Save').onClick(() => { this.close(); this.onSubmit(value); }));
  }
  onClose() { this.contentEl.empty(); }
}
