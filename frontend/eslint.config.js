import js from "@eslint/js";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import globals from "globals";

export default [
  {
    ignores: [
      "dist/**",
      "dist_temp/**",
      "node_modules/**",
      "public/**",
      "**/*.min.js",
      "prerender.mjs",
    ],
  },
  js.configs.recommended,
  {
    files: ["src/**/*.{js,jsx}"],
    plugins: {
      react,
      "react-hooks": reactHooks,
    },
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.es2022,
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    rules: {
      // React JSX integration so JSX tags mark identifiers as used
      ...react.configs.recommended.rules,
      ...react.configs["jsx-runtime"].rules,

      // STRICT: Catch undeclared variables and missing imports (strictly prevents ReferenceError)
      "no-undef": "error",
      "react/jsx-no-undef": "error",
      "no-empty": ["warn", { allowEmptyCatch: true }],
      "no-useless-escape": "warn",
      "no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
      "react/prop-types": "off",
      "react/no-unescaped-entities": "off",
      "react/no-unknown-property": "off",
      "no-constant-condition": ["warn", { checkLoops: false }],
    },
  },
  {
    // Node / Vite configuration files
    files: ["*.js", "*.mjs"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.node,
      },
    },
    rules: {
      "no-undef": "error",
    },
  },
];
