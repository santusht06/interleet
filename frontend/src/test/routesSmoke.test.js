import { describe, it, expect } from "vitest";

describe("Application Routes & Components Smoke Test", () => {
  const routes = [
    { name: "IndexPage", importFn: () => import("@/pages/index") },
    { name: "LoginPage", importFn: () => import("@/pages/login") },
    { name: "SignupPage", importFn: () => import("@/pages/signup") },
    { name: "DashboardPage", importFn: () => import("@/pages/app/dashboard") },
    { name: "ChallengesPage", importFn: () => import("@/pages/app/challenges/index") },
    { name: "ChallengeDetailPage", importFn: () => import("@/pages/app/challenges/$id") },
    { name: "EditorPage", importFn: () => import("@/pages/app/editor.$id") },
    { name: "LeaderboardPage", importFn: () => import("@/pages/app/leaderboard") },
    { name: "SettingsPage", importFn: () => import("@/pages/app/settings") },
    { name: "SystemDesignPage", importFn: () => import("@/pages/app/system-design") },
    { name: "StorePage", importFn: () => import("@/pages/app/Store") },
    { name: "BrowserPreview", importFn: () => import("@/pages/app/editor/BrowserPreview") },
    { name: "MonacoEditor", importFn: () => import("@/pages/app/editor/MonacoEditor") },
    { name: "ConsoleOutput", importFn: () => import("@/pages/app/editor/ConsoleOutput") },
  ];

  routes.forEach(({ name, importFn }) => {
    it(`loads ${name} without throwing ReferenceError or module evaluation errors`, async () => {
      const module = await importFn();
      expect(module).toBeDefined();
      expect(module.default || Object.keys(module).length > 0).toBeTruthy();
    });
  });
});
