import { theme as chakraTheme } from "@chakra-ui/react";
import { extendTheme } from "@chakra-ui/react";

const fonts = {
  ...chakraTheme.fonts,
  body: `Dubai,Oxygen,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"`,
  heading: `Dubai,Oxygen,Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol"`,
};

const breakpoints = {
  sm: "450px",
  md: "600px",
  lg: "800px",
  xl: "1000px",
  xxl: "1200px",
  "2xl": "1500px",
  "3xl": "1980px",
  "4xl": "2480px",
};

const overrides = {
  ...chakraTheme,
  fonts,
  breakpoints,
  fontWeights: { light: 200, normal: 400, medium: 500, bold: 700 },
  fontSizes: {
    xs: "12px",
    sm: "14px",
    md: "16px",
    lg: "18px",
    xl: "20px",
    "2xl": "24px",
    "3xl": "28px",
    "4xl": "32px",
    "5xl": "36px",
    "6xl": "48px",
    "7xl": "64px",
  },
  components: {
    Popover: {
      sizes: {
        xs: {
          w: "20px",
        },
      },
    },
  },
};

const customTheme = extendTheme(overrides);

export default customTheme;
