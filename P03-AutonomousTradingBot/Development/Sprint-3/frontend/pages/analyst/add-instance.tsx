import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import BotCard from '../../components/cards/BotCard';
import AnalystLayout from '../../components/layouts/AnalystLayout';

const AddInstance: NextPage = () => {
	const router = useRouter();

	return (
		<AnalystLayout>
			<div className='hero min-h-screen'>
				<div className='hero-content text-center'>
					<div className='max-w-xl'>
						<h1 className='text-5xl font-bold'>Add instance</h1>
					</div>

					<div className='flex items-start'>
						<div className=' px-8'>
							<BotCard
								desc='Add a trading instance to the selected investor and enter the required information to start running the bot for the investor.'
								label='Add Trading Instance'
								pathname={'/analyst/instance-params'}
								investor_id={router.query.investor_id as string}
							/>
						</div>
						<div className='col-sm-6 '>
							<BotCard
								desc='View all currently running bots for the selected investor.'
								label='View Instances'
								pathname={'/analyst/view-instances'}
								investor_id={router.query.investor_id as string}
							/>
						</div>
					</div>
				</div>
			</div>
		</AnalystLayout>
	);
};

export default AddInstance;
