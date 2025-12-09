'use client';

interface Contact {
  phone: string;
  email: string;
  address?: string;
}

interface ContactBlockProps {
  contact: Contact;
  layout?: 'vertical' | 'horizontal';
}

export function ContactBlock({ contact, layout = 'vertical' }: ContactBlockProps) {
  const isHorizontal = layout === 'horizontal';

  return (
    <section className="py-16 px-4">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">Contact Us</h2>
        <div className={`${isHorizontal ? 'flex flex-wrap justify-center gap-8' : 'space-y-6'}`}>
          <div className="text-center">
            <h3 className="font-semibold mb-2">Phone</h3>
            <a href={`tel:${contact.phone}`} className="text-blue-600 hover:underline">
              {contact.phone}
            </a>
          </div>
          <div className="text-center">
            <h3 className="font-semibold mb-2">Email</h3>
            <a href={`mailto:${contact.email}`} className="text-blue-600 hover:underline">
              {contact.email}
            </a>
          </div>
          {contact.address && (
            <div className="text-center">
              <h3 className="font-semibold mb-2">Address</h3>
              <p className="text-gray-600">{contact.address}</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
