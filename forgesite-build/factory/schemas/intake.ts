import { z } from 'zod';

export const BusinessIntakeSchema = z.object({
  businessName: z.string().min(1),
  ownerName: z.string().optional(),
  tradeType: z.enum([
    'builder',
    'remodeler',
    'cabinet_shop',
    'steel_buildings',
    'hvac',
    'electrical',
    'plumbing',
    'other'
  ]),
  serviceArea: z.string(),
  services: z.array(z.string()),
  typicalJobSize: z.string().optional(),
  idealClientDescription: z.string().optional(),
  differentiators: z.array(z.string()).optional(),
  testimonials: z.array(z.object({
    name: z.string(),
    quote: z.string(),
    projectType: z.string().optional()
  })).optional(),
  logoUrl: z.string().url().optional(),
  brandColors: z.object({
    primary: z.string().optional(),
    secondary: z.string().optional(),
    accent: z.string().optional()
  }).optional(),
  brandVoice: z.enum([
    'straightforward',
    'premium',
    'friendly',
    'no_bullshit'
  ]).default('straightforward'),
  mainGoal: z.enum([
    'get_leads',
    'look_legit',
    'recruit_staff',
    'showcase_projects'
  ]),
  contact: z.object({
    phone: z.string(),
    email: z.string().email(),
    address: z.string().optional()
  }),
  packageLevel: z.enum(['basic', 'pro', 'premium']).default('basic')
});

export const SiteConfigSchema = z.object({
  business: BusinessIntakeSchema,
  pages: z.array(z.object({
    route: z.string(),
    title: z.string(),
    modules: z.array(z.object({
      type: z.string(),
      props: z.record(z.any())
    }))
  })),
  seo: z.object({
    title: z.string(),
    description: z.string(),
    keywords: z.array(z.string()).optional()
  })
});

export type BusinessIntake = z.infer<typeof BusinessIntakeSchema>;
export type SiteConfig = z.infer<typeof SiteConfigSchema>;
