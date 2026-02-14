import path from 'path';
import fs from 'fs';

function loadTicks(logPath) {
  const lines = fs.readFileSync(logPath, "utf8").trim().split("\n");

  const ticks = [];

  for (const line of lines) {
    const entry = JSON.parse(line);

    if (entry.typ === "VIEW") {
      ticks.push(entry.msg[0]);
    }
  }

  return ticks;
}


const submissionId = process.argv[2];
if (!submissionId) {
  console.error("Usage: node replay-viewer.js <SUBMISSION_ID>");
  process.exit(1);
}

const logPath = path.join(".submissions", submissionId, "log.txt");
if (!fs.existsSync(logPath)) {
  console.error("Log file not found:", logPath);
  process.exit(1);
}

const outPath = path.join(".submissions", submissionId, "ticks.json");

fs.writeFileSync(outPath, JSON.stringify(loadTicks(logPath)));
